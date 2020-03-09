# applestore
這題購買的物品會用 linklist 存起來，而在 checkout 時如果總金額是 7174 的話會把 stack 上的東西用 linklist 做儲存
```
unsigned int checkout()
{
  int v1; // [esp+10h] [ebp-28h]
  char *v2; // [esp+18h] [ebp-20h]
  int v3; // [esp+1Ch] [ebp-1Ch]
  unsigned int v4; // [esp+2Ch] [ebp-Ch]

  v4 = __readgsdword(0x14u);
  v1 = cart();
  if ( v1 == 7174 )
  {
    puts("*: iPhone 8 - $1");
    asprintf(&v2, "%s", "iPhone 8");
    v3 = 1;
    insert(&v2);
    v1 = 7175;
  }
```
而我們就可以改變 stack 上的值去建假的 linklist。
而在 cart 會把 linklist 上的東西印出來，就可以把 stack 值改成 `libc_start_got` 位置讓他印來去拿到 libc 位置。
因為他使用 linklist ，因此我們要建假的 linklist 要有 stack 上的位置。
stack 位置可以在 `l.sym.environ` 拿到，這以前沒有碰過QQ。之後就很簡單去建假的 chunk 讓他改掉 got 即可。

