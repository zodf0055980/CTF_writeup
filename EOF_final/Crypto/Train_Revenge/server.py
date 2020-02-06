#!/usr/bin/env python3
from BlockCipher import RSA
from Crypto.Util.number import *

with open('flag', 'rb') as f:
    flag = f.read()
    flag = f'{int.from_bytes(flag, "big"):096b}'

def genkeys():
    e = 65537
    while True:
        p, q = getPrime(512), getPrime(512)
        n, phi = p * q, (p - 1) * (q - 1)
        if GCD(e, phi) == 1:
            d = inverse(e, phi)
            return (n, e), (n, d)

def menu():
    print(f'{"Want to buy some train tickets? ":=^20}')
    print('1) your ticket')
    print('2) use ticket')
    print('3) exit')

def show(rsa):
    (n, e), c = rsa.pub, rsa.encrypt(f'date:2020/02/05|secret:{flag}'.encode())
    print(f'n = {n}')
    print(f'e = {e}')
    print(f'ticket = {c.hex()}')

def use(rsa):
    cipher = bytes.fromhex(input('ticket = '))
    try:
        plain = rsa.decrypt(cipher)
        fields = plain.split(b'|')
        date, session = b'', b''
        for field in fields:
            key, _, value = field.partition(b':')
            if key == b'date':
                date = value
        if date == b'2020/02/05':
            print('Pass')
        else:
            print('Wrong ticket')
    except:
        print('Oops, our train has some technical issue')

def main():
    rsa = RSA.new(genkeys(), RSA.MODE_ECB)
    while True:
        menu()
        cmd = input('> ')
        if cmd == '1':
            show(rsa)
        elif cmd == '2':
            use(rsa)
        else:
            print('I have spoken')
            return

main()
