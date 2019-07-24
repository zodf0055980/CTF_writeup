# 解答
```shell
gdb-peda$ r
Starting program: /home/yuan/ctf/ns107/ret2shellcode/ret2shellcode 
##############################
Hello~~
buffer address: 0x7fffffffde60
##############################
Input:
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
bye~

Program received signal SIGSEGV, Segmentation fault.

[----------------------------------registers-----------------------------------]
RAX: 0x0 
RBX: 0x0 
RCX: 0x7ffff7af4154 (<__GI___libc_write+20>:	cmp    rax,0xfffffffffffff000)
RDX: 0x7ffff7dd18c0 --> 0x0 
RSI: 0x7ffff7dd07e3 --> 0xdd18c0000000000a 
RDI: 0x1 
RBP: 0x6161616161616161 ('aaaaaaaa')
RSP: 0x7fffffffdf38 ('a' <repeats 72 times>)
RIP: 0x40073e (<main+199>:	ret)
R8 : 0x4 
R9 : 0x7ffff7fe24c0 (0x00007ffff7fe24c0)
R10: 0x3 
R11: 0x246 
R12: 0x400590 (<_start>:	xor    ebp,ebp)
R13: 0x7fffffffe010 --> 0x1 
R14: 0x0 
R15: 0x0
EFLAGS: 0x10202 (carry parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x400733 <main+188>:	call   0x400550 <puts@plt>
   0x400738 <main+193>:	mov    eax,0x0
   0x40073d <main+198>:	leave  
=> 0x40073e <main+199>:	ret    
   0x40073f:	nop
   0x400740 <__libc_csu_init>:	push   r15
   0x400742 <__libc_csu_init+2>:	push   r14
   0x400744 <__libc_csu_init+4>:	mov    r15,rdx
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdf38 ('a' <repeats 72 times>)
0008| 0x7fffffffdf40 ('a' <repeats 64 times>)
0016| 0x7fffffffdf48 ('a' <repeats 56 times>)
0024| 0x7fffffffdf50 ('a' <repeats 48 times>)
0032| 0x7fffffffdf58 ('a' <repeats 40 times>)
0040| 0x7fffffffdf60 ('a' <repeats 32 times>)
0048| 0x7fffffffdf68 ('a' <repeats 24 times>)
0056| 0x7fffffffdf70 ('a' <repeats 16 times>)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x000000000040073e in main ()
```
用 RSP - buffer address 取得 buffer 大小
