from pwn import *

ip = "bamboofox.cs.nctu.edu.tw"
port = "11016"
r = remote(ip, port)

r.recvuntil("base64\n")
elf = r.recvuntil("\n\n").decode('base64')
f = open("elf", "wb")
f.write(elf)
f.close()

oo = []
ooo = []
oooo = []
print 'file ok'

oo_count = 0x20393b
for i in range(10) :
    todo = 'objdump -d -M intel elf | grep \'DWORD PTR \[rip+'+hex(oo_count)+'\''
    output = os.popen(todo)
    a = output.read()
    h = a[64:70].rstrip()
    oo .append(int(h.upper(), 16))
    oo_count -= 6
print oo

ooo_count = 0x203737
for i in range(100) :
    todo = 'objdump -d -M intel elf | grep \'DWORD PTR \[rip+'+hex(ooo_count)+'\''
    output = os.popen(todo)
    a = output.read()
    h = a[64:70].rstrip()
    ooo .append(int(h.upper(), 16))
    ooo_count -= 6
print ooo

oooo_count = 0x20352f
for i in range(1000) :
    todo = 'objdump -d -M intel elf | grep \'DWORD PTR \[rip+'+hex(oooo_count)+'\''
    output = os.popen(todo)
    a = output.read()
    h = a[64:70].rstrip()
    oooo .append(int(h.upper(), 16))
    oooo_count -= 6

print "create ok"
print r.recvline()
print r.recvline()
for i in range(10) :
    r.sendline(str(oo[i]))
print r.recvline()
for i in range(100) :
    r.sendline(str(ooo[i]))
print r.recvline()
for i in range(1000) :
    r.sendline(str(oooo[i]))
print r.recvline()

r.interactive()

# $ cat /home/ctf/flag
# CTF{o_oo_ooo_th1s_1s_how_simple_acg_look_like}
