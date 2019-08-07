# $ mkvirtualenv angr
# $ pip install angr
# $ pip install pwn

from pwn import *
import angr

ip = "bamboofox.cs.nctu.edu.tw"
port = "11015"
r = remote(ip, port)

r.recvuntil("base64\n")
elf = r.recvuntil("\n\n").decode('base64')
f = open("elf1", "wb")
f.write(elf)
f.close()

print "angr start   1"

ag1 = angr.Project("./elf1")
pa1 = ag1.factory.simulation_manager().explore(find=0x0040079f)
res1 = pa1.found[0].state.posix.dumps(0)

print  res1

r.recvuntil("0th Piece\n")
r.sendline(str(res1[0:2]))
print r.recvline()
r.sendline(str(res1[3:5]))
print r.recvline()
r.sendline(str(res1[6:8]))
print r.recvline()
r.sendline(str(res1[9:11]))
print r.recvline()
r.sendline(str(res1[12:14]))
print r.recvline()
r.sendline(str(res1[15:17]))
print r.recvline()
r.sendline(str(res1[18:20]))
print r.recvline()
r.sendline(str(res1[21:23]))
print r.recvline()
r.sendline(str(res1[24:26]))
print r.recvline()

elf = r.recvuntil("\n\n").decode('base64')
f = open("elf2", "wb")
f.write(elf)
f.close()

print "angr start   2"

ag2 = angr.Project("./elf2")
pa2= ag2.factory.simulation_manager().explore(find=0x0040079f)
res2 = pa2.found[0].state.posix.dumps(0)

print  res2

r.recvuntil("0th Piece\n")
r.sendline(str(res2[0:2]))
print r.recvline()
r.sendline(str(res2[3:5]))
print r.recvline()
r.sendline(str(res2[6:8]))
print r.recvline()
r.sendline(str(res2[9:11]))
print r.recvline()
r.sendline(str(res2[12:14]))
print r.recvline()
r.sendline(str(res2[15:17]))
print r.recvline()
r.sendline(str(res2[18:20]))
print r.recvline()
r.sendline(str(res2[21:23]))
print r.recvline()
r.sendline(str(res2[24:26]))
print r.recvline()