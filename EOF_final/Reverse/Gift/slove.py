from pwn import *
import gzip
import os

while(1):
    with gzip.open('gift.gz', 'rb') as f:
        file_content = f.read()
    out = open("gift","w")
    out.write(file_content)
    out.close()
    os.system("chmod 774 gift")

    r = process('./gift')
    p = open('./gift' , 'r')
    offset = 0x8b0 + 72
    password = p.read()[offset:offset+256]
    r.recv()
    r.send(password)
    print password

    out = open("gift.gz","w")
    r.recvuntil("good\n")
    t = r.recvall()
    out.write(t)
    out.close()
