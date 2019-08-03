#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import base64

ip = "bamboofox.cs.nctu.edu.tw"
port = 22006
r = remote(ip,port)

f1 = open('shattered-1.pdf','r')
p1 = f1.read()
b1 = base64.b64encode(p1)
print b1
print "b1 ok\n"
f2 = open('shattered-2.pdf','r')
p2 = f2.read()
b2 = base64.b64encode(p2)
print "b2 ok\n"
print b2

r.recvuntil('username:\n')
r.sendline(b1)
r.recvuntil('password:\n')
r.sendline(b2)

flag = r.recvline()
print flag