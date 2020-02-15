# hacknote

重點在 delete
```
unsigned int sub_80487D4()
{
  int index; // [esp+4h] [ebp-14h]
  char buf; // [esp+8h] [ebp-10h]
  unsigned int canary; // [esp+Ch] [ebp-Ch]

  canary = __readgsdword(0x14u);
  printf("Index :");
  read(0, &buf, 4u);
  index = atoi(&buf);
  if ( index < 0 || index >= index_size )
  {
    puts("Out of bound!");
    _exit(0);
  }
  if ( ptr[index] )
  {
    free(*(ptr[index] + 1));
    free(ptr[index]);
    puts("Success");
  }
  return __readgsdword(0x14u) ^ canary;
}
```
可以看到 free 完並沒有把 ptr 給設成 Null。所以之後仍然可以去用到先前被 free 的東西。接下來看 malloc

```
ptr[i] = malloc(8u);
if ( !ptr[i] )
{
  puts("Alloca Error");
  exit(-1);
}
*ptr[i] = fun;
printf("Note size :");
read(0, &buf, 8u);
size = atoi(&buf);
v0 = ptr[i];
v0[1] = malloc(size);
if ( !*(ptr[i] + 1) )
{
  puts("Alloca Error");
  exit(-1);
}
printf("Content :");
read(0, *(ptr[i] + 1), size);
puts("Success !");
++index_size;
return __readgsdword(0x14u) ^ canary;
```
他會去 malloc 兩塊區域，第一塊存 fun function 和內容的位置，我們這邊建立兩塊 0x20 note heap 會長這樣

|  | size | 內容 | 內容 | 
| -------- | -------- | -------- | -------- |
| 0-1 | 0x10     | put_addr  | addr_to_1 |
| 0-2 | 0x20     | Text   | -------- |
| 1-1 | 0x10     | put_addr   | addr_to_1 |
| 1-2 | 0x20     | Text   | -------- |

之後 free 掉那兩塊， 0x10 fast bin 會長這樣 ： 1-1 -> 0-1

而這時我們去 malloc 大小是 8 的一塊的話，會去拿到 fastbin 的內容 ，並且去修改到第 2 塊成下面這樣。

|  | size | 內容 | 內容 | 
| -------- | -------- | -------- | -------- |
| 0-1 | 8     | put_addr  | GOT_addr |
| 0-2 | 0x20     | Text   | -------- |
| 1-1 | 8     | put_addr   | addr_to_2-2 |
| 1-2 | 0x20     | Text   | -------- |
| 2-1 | 8     |  指向 0-1  |  |
| 2-2 | 8     |   指向 1-1 |  |

這時去印出第 0 塊，就會拿到 GOT 的內容。之後再把第二塊 free 掉，0x10 fast bin 會長這樣 ： 1-1 -> 0-1

之後再去建立 malloc 大小是 8 的 note 的話，就可以在改到 0-1 的內容，把它改成 system 的位置即可。(onegadget 都不能用 = =)。如果想要拿 sh ，可以傳進去 `\x0ash\x00` `;ash\x00`  `||sh` (因為字串前面會垃圾，這樣才能執行) 
