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

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

modin = modinv(16,n)
m = 0
de = 0

for i in range(size(n) // 4):
    q = dec( pow( modin , i * e , n ) * c %n )
    x = ( q - ( modin * de ) % n ) % 16
    de = ( modin * de + x) % n
    m = pow( 16 , i ) * x + m
    print(m)

print(long_to_bytes(m))