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

def decrypt(ctx , key) :
    N , ksz = len(charset), len(key)
    return ''.join(charset[(c - key[i % ksz]) % N] for i ,c in enumerate(ctx))

def toprintable(data):
    a = ""
    for i in range(len(data)):
        if 32 <=  ord(data[i]) < 127 :
            a += data[i]
        else:
            a += '_'
    return a

# load data
with open("./output.txt") as f:
    ctx = f.readline().strip()[4:]
    enc = bytes.fromhex(f.readline().strip()[6:])
ctx = [charset_idmap[c] for c in ctx]

with open("./ngrams.json") as f:
    ngrams = json.load(f)

@fn.lru_cache(1000)
def get_trigam(x) :
    x= ''.join(x)
    y = ngrams.get(x)
    if y is not None:
        return y
    ys = []
    a, b = ngrams.get(x[:2]) , ngrams.get(x[2:])
    if a is not None and b is not None:
        ys.append(a + b)
    a, b = ngrams.get(x[:1]) , ngrams.get(x[1:])
    if a is not None and b is not None:
        ys.append(a + b)
    if len(ys) :
        return max(ys)
    if any(c not in ngrams for c in x) :
        return -25
    return sum(map(ngrams.get , x))


@fn.lru_cache(1000)
def fitness(a):
    plain = decrypt(ctx , a)
    tgs = zip(plain , plain[1:], plain[2:])
    score = sum(get_trigam(tg) for tg in tgs)
    return score

def initialize(size) :
    populate = []
    for i in range(size):
        key = tuple(random.randrange(len(charset)) for _ in range(ksz))
        populate.append(key)
    return populate

def crossover( a , b , prob):
    r= list(a)
    for i in range(len(r)):
        if random.random() < prob:
            r[i] = b[i]
    return tuple(r)

def mutate(a):
    r = list(a)
    i = random.randrange(len(a))
    r[i] = random.randrange(len(charset))
    return tuple(r)

def takeSecond(elem):
    return elem[1]

number = 10
seedpool = initialize(number)
seed = []

rangeseed = []
for i in range(len(seedpool)):
    rangeseed.append( ( seedpool[i] , fitness(seedpool[i]) ) )
rangeseed.sort(key=takeSecond , reverse=True)

for _ in range(10):
    seed.clear()
    for i in range(number):
         seed.append(rangeseed[i][0])
    for i in range(100):
        k = random.randrange(number)
        re = mutate(seed[k])
        seed.append(re)
    for i in range(100):
        k1 = random.randrange(number)
        k2 = random.randrange(number)
        k3 = random.randrange(ksz)
        re = crossover(seed[k1],seed[k2],k3)
        seed.append(re)

    rangeseed.clear()
    for i in range(len(seed)):
        rangeseed.append( ( seed[i] , fitness(seed[i]) ) )
    rangeseed.sort(key=takeSecond , reverse=True)
    print('best = %d , c = %s' % (rangeseed[0][1] , decrypt(ctx,rangeseed[0][0]) ))

# key =  (28, 38, 1, 15, 1, 24, 34, 16, 18, 18, 5, 12, 19, 6, 21, 7, 29, 30, 22, 37, 37, 7, 22, 14, 31, 25, 11, 1, 28, 36, 27, 26, 20, 0, 35, 25, 25, 5, 23, 24, 35, 30, 38, 19, 28, 16, 36, 14, 11, 16, 6, 15, 17, 5, 9, 31, 32, 23, 23, 20, 13, 25, 11, 19, 18, 35, 3, 35, 30, 26, 21, 35, 8, 21, 25, 29, 18, 31, 18, 8)
key = rangeseed[0][0]
c = decrypt(ctx,key)
print(toprintable(c))
pan = "according to cnn, when researchers were asked what their language of choice was, 10 percent of the unicorns chose english. the other 60 percent of the unicorns culse a language that could olt be given a simple answer. the research says that more than a third of unicorop only use english. some are even creating whole language systems."

k = hashlib.sha512( ''.join(charset[k] for k in key ).encode('ascii') ).digest()
dec = bytes( ci ^ ki for ci,ki in zip(enc , k) )
print('dec = ',dec)