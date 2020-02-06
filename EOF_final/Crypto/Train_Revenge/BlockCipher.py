#!/usr/bin/env python3
import os
import random

class RSA:
    MODE_ECB = 0

    def __init__(self, key, mode):
        self.pub = key[0]
        self.pri = key[1]
        self.mode = mode

    @classmethod
    def new(cls, key, mode):
        return cls(key, mode)

    @staticmethod
    def parity(data):
        return f'{int.from_bytes(data, "big"):b}'.count('1') % 2

    def pad(self, data):
        l = 128 - 2 - len(data)
        while True:
            checksum = bytes([random.choice(b'01') for _ in range(l)])
            result = b'\x00' + checksum + b'\x00' + data
            if self.parity(result) == 0:
                return result

    def unpad(self, data):
        if self.parity(data) != 0:
            raise ValueError('Checksum Error')
        start = data[1:].find(b'\x00') + 2
        return data[start:]

    def encrypt(self, plain):
        n, e = self.pub
        cipher = b''
        if self.mode == self.MODE_ECB:
            cipher = b''
            for i in range(0, len(plain), 128-3):
                x = int.from_bytes(self.pad(plain[i:i+128-3]), 'big')
                y = pow(x, e, n)
                z = y.to_bytes(128, 'big')
                cipher += z
        else:
            raise NotImplementedError
        return cipher

    def decrypt(self, cipher):
        n, d = self.pri
        plain = b''
        if self.mode == self.MODE_ECB:
            for i in range(0, len(cipher), 128):
                x = int.from_bytes(cipher[i:i+128], 'big')
                y = pow(x, d, n)
                z = self.unpad(y.to_bytes(128, 'big'))
                plain += z
        else:
            raise NotImplementedError
        return plain
