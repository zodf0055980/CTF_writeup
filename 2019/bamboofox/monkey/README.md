# 解法
如果直接用gdb 在
```
void print_monkey(void)
{
    system("cat /home/ctf/graph");
}
```
會因為 system 的緣故進行fork，而 GDB 一開始預設是 follow child。
因此可以在 gdb 中輸入
set follow-fork-mode parent
[參考資料](https://sourceware.org/gdb/current/onlinedocs/gdb/Forks.html)

看到 `printf(temp);` 明顯知道可以透過 fmt 去改值
first:
一開始想要去改 exit_got 到 flag() 裡的打開 flag，但是在 `fscanf(fp,"%s",flag);`會去改到 canary 的值而失敗
second:
因為先執行 main() 而後執行 program() 會去儲存在 main frame 的 $ebp 因此可以可以透過 leak 先前 frame stack 的位置去取得 banana 的位置。在透過 fmt 去改他的值。
