import random
import json
import functools as fn
import numpy as np
import readline
import string
import hashlib

charset = string.ascii_lowercase + string.digits + ',. '
charset_idmap = { e : i for i ,e in enumerate(charset)}

ksz = 80

with open("./output.txt") as f:
    ctx = f.readline().strip()[4:]
    enc = bytes.fromhex(f.readline().strip()[6:])

lis = list(charset)
ctx = [charset_idmap[c] for c in ctx]
key = (28, 38, 1, 15, 1, 24, 34, 16, 18, 18, 5, 12, 19, 6, 21, 7, 29, 30, 22, 2, 4, 7, 22, 14, 31, 25, 11, 1, 3, 11, 3, 26, 20, 0, 35, 25, 25, 5, 23, 24, 34, 10, 18, 30, 32, 16, 36, 14, 11, 16, 6, 15, 17, 5, 9, 31, 32, 23, 23, 23, 18, 25, 31, 24, 36, 26, 4, 16, 38, 1, 33, 15, 23, 24, 28, 29, 18, 31, 18, 8)
N , ksz = len(charset), len(key)
pan = "according to cnn, when researchers were asked what their language of choice was, 10 percent of the unicorns chose english. the other 60 percent of the unicorns culse a language that could olt be given a simple answer. the research says that more than a third of unicorop only use english. some are even creating whole language systems."

count = 0
ll = []
for i in range(len(key)):
    do = (ctx[i] - key[i % ksz]) % N
    p = charset[do]
    a = lis.index(pan[i])
    b = lis.index(p)
    ll.append( (key[i] - (a - b ) )% N)
print(ll)
