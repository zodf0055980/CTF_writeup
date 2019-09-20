#!/usr/bin/env python3
from sympy import *
import random




op3_non = [[2, 11, 8, 5, 7, 12, 6, 13, 14, 9, 3, 10, 15, 1, 0, 4]]
op3_rev = [14, 13, 0, 10,15,3 ,6 ,4 ,2 ,9 ,11 ,1 ,5 ,7 ,8,12 ]
op4_rev = [141,154,50,242,39,72,47,160,147,196,235,67,146,149,155,4,208,193,42,101,32,70,224,210,244,109,29,197,199,86,73,49,60,126,79,153,69,182,140,143,44,115,144,194,27,51,84,98,206,249,202,227,43,234,158,176,64,184,28,156,157,201,219,12,94,172,46,85,41,198,78,30,34,91,134,11,6,58,10,129,254,190,255,130,239,103,222,16,142,108,161,127,111,192,171,92,62,107,122,200,131,228,56,33,229,237,105,188,54,37,75,185,102,168,52,164,81,20,99,124,175,128,252,178,18,191,116,118,151,159,40,53,253,90,212,205,7,17,148,21,22,117,113,48,221,77,179,15,181,120,76,240,220,133,166,135,88,110,216,104,25,225,80,38,9,217,63,114,211,183,245,26,203,247,87,218,139,209,123,1,95,83,163,19,100,223,177,162,226,65,0,167,14,248,187,93,236,180,246,61,232,23,214,125,13,215,233,204,89,150,165,132,169,24,250,82,3,59,66,137,35,138,241,119,96,213,74,45,231,112,186,136,57,55,238,170,145,8,230,106,5,97,2,71,121,174,36,31,195,173,68,152,243,207,189,251]
def op1(p, s):
    return sum([i * j for i, j in zip(s, p)]) % 256

def op2(m, k):
    return bytes([i ^ j for i, j in zip(m, k)])

def op3(m, p):
    return bytes([m[p[i]] for i in range(len(m))])

def op4(m, s):
    return bytes([s[x] for x in m])

def deop1(p, s):
    return sum([i * j for i, j in zip(s, p)]) % 256

def deop2(m, k):
    return bytes([i ^ j for i, j in zip(m, k)])

def deop3(m, p):
    ss = [m[op3_rev[i]] for i in range(len(m))]
    return bytes(ss)

def deop4(m, s):
    s4 = [op4_rev[x] for x in m]
    return bytes(s4)

'''
Linear Feedback Shift Register
'''
def destage0(m):
    random.seed('oalieno')
    p = [int(random.random() * 256) for i in range(16)]
    s = [int(random.random() * 256) for i in range(16)]
    c = b''
    for x in m:
        k = op1(p, s)
        c += bytes([x ^ k])
        s = s[1:] + [k]
    return c

def stage0(m):
    random.seed('oalieno')
    p = [int(random.random() * 256) for i in range(16)]
    s = [int(random.random() * 256) for i in range(16)]
    c = b''
    for x in m:
        k = op1(p, s)
        c += bytes([x ^ k])
        s = s[1:] + [k]
    return c

'''
Substitution Permutation Network
'''
def destage1(m):
    random.seed('oalieno')
    k = [int(random.random() * 256) for i in range(16)]
    p = [i for i in range(16)]
    random.shuffle(p)
    s = [i for i in range(256)]
    random.shuffle(s)
    c = m
    for i in range(16):
        c = deop4(c, s)
        c = deop3(c, p)
        c = deop2(c, k)
    return c


def stage1(m):
    random.seed('oalieno')
    k = [int(random.random() * 256) for i in range(16)]
    p = [i for i in range(16)]
    random.shuffle(p)
    s = [i for i in range(256)]
    random.shuffle(s)
    c = m
    for i in range(16):
        c = op2(c, k)
        c = op3(c, p)
        c = op4(c, s)
    return c

def decrypt(m, key):
    stage = [destage0, destage1]
    for i in map(int, f'{key:08b}'):
        m = stage[i](m)
    return m

def encrypt(m, key):
    stage = [stage0, stage1]
    for i in map(int, f'{key:08b}'):
        m = stage[i](m)
    return m

if __name__ == '__main__':
    enc = open('cipher', 'rb').read()
    for i in range(0,255):
        print(chr(i))
        key = bytes(chr(i) , encoding='utf-8')
        print(i)
        print(key)
        end = decrypt(enc, int.from_bytes(key, 'little'))
        print(end)
