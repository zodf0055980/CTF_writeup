# calc
先把 clac 的函數命名一下，並依照 initpool() 去改變數大小
```
unsigned int calc()
{
  int int_pool[101]; // [esp+18h] [ebp-5A0h]
  char get_strings[1024]; // [esp+1ACh] [ebp-40Ch]
  unsigned int canary; // [esp+5ACh] [ebp-Ch]

  canary = __readgsdword(0x14u);
  while ( 1 )
  {
    bzero(get_strings, 1024u);
    if ( !get_expr((int)get_strings, 1024) )
      break;
    init_pool(int_pool);
    if ( parse_expr((int)get_strings, int_pool) )
    {
      printf((const char *)&d, int_pool[int_pool[0] - 1 + 1]);
      fflush(stdout);
    }
  }
  return __readgsdword(0x14u) ^ canary;
}
```
其中 get_expr 是去篩掉除了 `+-*/%0-9` 的字元，接著看 parse_expr

parse_expr 是去把數字和符號給隔開，並做運算，這邊看運算函數 eval
```
_DWORD *__cdecl eval(_DWORD *int_pool, char op)
{
  _DWORD *result; // eax

  if ( op == '+' )
  {
    int_pool[*int_pool - 1] += int_pool[*int_pool];
  }
  else if ( op > '+' )
  {
    if ( op == '-' )
    {
      int_pool[*int_pool - 1] -= int_pool[*int_pool];
    }
    else if ( op == '/' )
    {
      int_pool[*int_pool - 1] /= int_pool[*int_pool];
    }
  }
  else if ( op == '*' )
  {
    int_pool[*int_pool - 1] *= int_pool[*int_pool];
  }
  result = int_pool;
  --*int_pool;
  return result;
}
```
這時候就要關心他 int_pool 的實做，他是把 `int_pool[0]` 當成計算 pool 中有幾個數字的 count，其他依序往下排。

而這時如果我們輸入 `+100` ， 就會出問題，他的 int_pool 會長這樣



| 0 | 1 | 
| -------- | -------- |
| 1     | 100     |

再來要去做 `+` 的處理，他的處理為 ` int_pool[*int_pool - 1] += int_pool[*int_pool];`
運算為 `int_pool[0] += int_pool[1]`


| 0 | 
| -------- | 
| 101     | 

在最後會執行 `--*int_pool` 因此會使 `int_pool[0]` = 100。
而在 calc 的 printf 是去印 `int_pool[int_pool[0]]` 也就是 `int_pool[100]` ，因此會造成 memory leak。
而如果輸入類似 `+100 + 1`，也會造成問題，他會先處理 `+300`，最後結果會變成:


| 0 | 
| -------- | 
| 100     | 

之後輸入 `1` ，而他加進 pool 的判斷為
```
v9 = atoi(s1);
if ( v9 > 0 )
{
    pool_count = (*int_pool)++;
    int_pool[pool_count + 1] = v9;
}
```
因此會變成


| 0 | ...| 100 | 101 |
| -------- | -------- | -------- | -------- |
| 101     | ...     | ? | 1 |

之後會再去做 `+` 的運算 ` int_pool[*int_pool - 1] += int_pool[*int_pool];`
因此會變成 `int_pool[100] += int_pool[101];`

| 0 | ...| 100 |
| -------- | -------- | -------- |
| 101     | ...     | ? +1 |

結合前面洩漏位置的值我們可以透過 `+-` 去改任意位置的值。
接下來會想要去串 ROP，但 ROP 會需要 `/bin/sh` 的位置，我選擇把他放到 stack 上，因此需要 stack 的位置。這時可以看前面 calc 的 stack 變數安排。
```
int int_pool[101]; // [esp+18h] [ebp-5A0h]
char get_strings[1024]; // [esp+1ACh] [ebp-40Ch]
unsigned int canary; // [esp+5ACh] [ebp-Ch]
```
由於是 32 bit ，因此 cannary 位置 `offset 為 101 + (1024 / 4) = 357`
並用 gdb 看位置的值
```
1452| 0xffffcc8c --> 0xcc163c00 
1456| 0xffffcc90 --> 0x0 
1460| 0xffffcc94 --> 0x80481b0 (<_init>:	push   ebx)
1464| 0xffffcc98 --> 0xffffccb8 --> 0x8049c30 (<__libc_csu_fini>:	push   ebx)
1468| 0xffffcc9c --> 0x8049499 (<main+71>:	mov    DWORD PTR [esp],0x80bf842)
1472| 0xffffcca0 --> 0x80ec200 --> 0xfbad2a84 
1476| 0xffffcca4 --> 0x8049434 (<timeout>:	push   ebp)
1480| 0xffffcca8 --> 0xffffcd4c --> 0xffffcf53 ("CLUTTER_IM_MODULE=xim")
1484| 0xffffccac --> 0x80481b0 (<_init>:	push   ebx)
1488| 0xffffccb0 --> 0x0 
1492| 0xffffccb4 --> 0x80ec00c --> 0x8069120 (<__stpcpy_sse2>:	mov    edx,DWORD PTR [esp+0x4])
1496| 0xffffccb8 --> 0x8049c30 (<__libc_csu_fini>:	push   ebx)

```
因此可以找到 `0xffffcc98` 放之前 rbp 的位置，offset 為 360。之後就能串 ROP 了。
