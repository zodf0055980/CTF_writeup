from pwn import *
from Crypto.Util.number import *

ip = "edu-ctf.csie.org"
port = 10192
r = remote(ip,port)

r.recv()
r.sendline('1')

exec(r.recvline())
exec(r.recvline())
exec(r.recvline())

def dec(c):
    r.recv()
    r.sendline('2')
    r.sendline(str(c))
    get = r.recvline().strip().decode()
    print(get)
    return int(get[4:])

def lsb(b, nn):
    L = 0
    H = n
    for x in b:
        i = -x * inverse(nn, 16) % 16
        D = H - L
        OL = L
        L = OL + i * D // 16
        H = OL + (i + 1) * D // 16
    return L

b = []
t = pow(16,e,n)

for _ in range(size(n) // 4 + 1):
    c = (t * c) % n
    b.append(dec(c))

for nn in range(1, len(b), 2):
    m = lsb(b, nn)
    print(m)
    flag = long_to_bytes(m)
    if b'FLAG' in flag:
        print(flag)
