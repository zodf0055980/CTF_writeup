#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

ip = "bamboofox.cs.nctu.edu.tw"
port = 22004
r = remote(ip,port)
win = ["paper","scissors","rock"]
hint = ['!','?',':']
first_get = r.recvline()
hint_get = first_get[17]
r.recvline()
number = 0
for i in range(0 , 3) :
    if(hint_get == hint[i]):
        number = i
for i in range(0 , 100) :
    r.recvuntil(':')
    r.sendline(win[number])
    number = (number + 1)%3
    r.recvline()
    r.recvline()
flag = r.recvline()
print flag