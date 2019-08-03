#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

ip = "bamboofox.cs.nctu.edu.tw"
port = 22005
r = remote(ip,port)


hight = 500000000
low = 0

r.recvuntil(' = ')
balance = (hight + low)/2
r.sendline(str(balance))    
a = r.recvline()
while( a[4] == 's' or a[4] ==  'b')  :
    if(a[4] == 's') :
        low = balance
    else :
        hight = balance
    r.recvuntil(' = ')
    balance = (hight + low)/2
    r.sendline(str(balance))    
    a = r.recvline()
print   r.recvline()

