import  struct
import sys, struct
from ctypes import *
from pwn import *
import time

l = CDLL( './libc-2.27.so' )
mask = 2 ** 32 -1

f = open("output.txt", 'rb').read()
time = f[-56:]
year = time[0:16]
mon = time[16:24]
wday = time[24:32]
hour = time[32:40]
tmin = time[40:48]
sec = time[48:56]
year = int(b''.join( struct.pack('<s', year[ i: i + 4]) for i in range(0,13,4)))
mon = int(b''.join( struct.pack('<s', mon[ i: i + 4]) for i in range(0,5,4)))
wday =  int(b''.join( struct.pack('<s', wday[ i: i + 4]) for i in range(0,5,4)))
hour =  int(b''.join( struct.pack('<s', hour[ i: i + 4]) for i in range(0,5,4)))
tmin =  int(b''.join( struct.pack('<s', tmin[ i: i + 4]) for i in range(0,5,4)))
sec =  int(b''.join( struct.pack('<s', sec[ i: i + 4]) for i in range(0,5,4)))
print("===time===")
print(year)
print(mon)
print(wday)
print(hour)
print(tmin)
print(sec)
mday = 11
print("======")

text = f[:-56]

ti = 1568179514
l.srand(ti)

def ichi(a):
    return  a ^ 0xFACEB00C

def ni(a):
    return  a - 74628

def san(a):
    x = (a & 0x55555555) >> 28 | ((a & 0x55555555) << 4 & mask)
    y =  (a & 0xaaaaaaaa) >> 2 | ((a & 0xaaaaaaaa) << 30 & mask)
    return   x | y

def yon(a):
    return ichi(ni(san(a)))

out = open("out","wb")
for i in range( 0 , len(text) , 4):
    a = u32(text[i:i + 4])
    r = l.rand() % 4
    if(r == 0):
        a = ichi(a)
    elif( r == 1 ):
        a = ni(a)
    elif( r == 2 ):
        a = san(a)
    elif( r == 3 ):
        a = yon(a)
    a = a  & mask
    out.write(p32(a))
