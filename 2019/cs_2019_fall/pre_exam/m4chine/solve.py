from ctypes import *
from binascii import *


class Machine:

    def __init__(self, init):
        self.context = list(map(ord, init))
        self.op = {0:self.add,  1:self.cmp,  2:self.context,  3:self.empty,  6:self.pop,  7:self.push,  8:self.sub,  9:self.terminal}

    def empty(self, _):
        print("empty")
        print(self.context)
        return len(self.context) == 0

    def e_start(self, code):
        for i in zip(*(iter(code),) * 2):
            if i != None:
                self.op[ord(i[0])](ord(i[1]))

    def push(self, num):
        self.context.append(num)
        print("push " + str(num))
        print(self.context)

    def pop(self, _):
        if len(self.context) < 1:
            raise SyntaxError('You should sharpen your coding skill')
        result, self.context = self.context[(-1)], self.context[:-1]
        print("pop")
        print(self.context)
        print(result)
        return result

    def terminal(self, _):
        if len(self.context) < 1:
            raise SyntaxError('You should sharpen your coding skill')
        if self.context[(-1)] == 0:
            print('You fail, try again')
            exit(0)
        print("success ")
        print(" ")
        print(" ")

    def add(self, _):
        if len(self.context) < 2:
            raise SyntaxError('You should sharpen your coding skill')
        result, self.context = self.context[(-1)] + self.context[(-2)], self.context[:-2]
        self.context.append(c_int8(result).value)
        print("add")
        print(self.context)

    def sub(self, _):
        if len(self.context) < 2:
            raise SyntaxError('You should sharpen your coding skill')
        result, self.context = self.context[(-1)] - self.context[(-2)], self.context[:-2]
        self.context.append(c_int8(result).value)
        print("sub")
        print(self.context)

    def cmp(self, num):
        if len(self.context) < 1:
            raise SyntaxError('You should sharpen your coding skill')
        self.context[-1] = 1 if self.context[(-1)] == num else 0
        print("cmp " + str(num))
        print(self.context)

#s =  chr(1)+chr(1)+chr(1)+chr(1)+chr(1)+chr(1)+chr(1)+ chr(48)+ chr(119)+ chr(95)+  chr(66)+ chr(105) + chr(105)+ chr(105) + chr(105)+ chr(105)+ chr(105) + chr(105)+ chr(105) + chr(71)+ chr(95) + chr(83) + chr(105) + chr(90) + chr(101) + chr(51) + chr(101) + chr(51) + chr(33) + chr(125)
s = 'FLAG{W0w_BiiiiiiiiG_SiZe3e3!}'
print(s)
emu = Machine(s)
print(emu.context)
emu.e_start('\x08\x00\x07\x08\x00\x00\x01d\t\x00\x00\x00\x014\t\x00\x073\x07\x01\x073\x08\x00\x00\x00\x01e\t\x00\x00\x00\x08\x00\x07c\x00\x00\x01\x00\t\x00\x00\x00\x074\x08\x00\x01\x00\t\x00\x06\x00\x01e\t\x00\x06\x00\x07Z\x08\x00\x01\x00\t\x00\x07h\x00\x00\x08\x00\x01\x00\t\x00\x06\x00\x07S\x08\x00\x01\x00\t\x00\x06\x00\x07_\x08\x00\x01\x00\t\x00\x06\x00\x07G\x08\x00\x01\x00\t\x00\x00\x00\x01j\t\x00\x00\x00\x01j\t\x00\x00\x00\x01j\t\x00\x00\x00\x01j\t\x00\x00\x00\x01j\t\x00\x00\x00\x01j\t\x00\x00\x00\x01j\t\x00\x00\x00\x01j\t\x00\x00\x00\x01C\t\x00\x06\x00\x07\x00\x07\x01\x00\x00\x07\x02\x00\x00\x07\x03\x00\x00\x07\x04\x00\x00\x07\x05\x00\x00\x07\x06\x00\x00\x07\x07\x00\x00\x07\x08\x00\x00\x07\t\x00\x00\x07\n\x00\x00\x07\x0b\x00\x00\x07\x0c\x00\x00\x07\r\x00\x00\x07\x04\x00\x00\x08\x00\x01\x00\t\x00\x06\x00\x01w\t\x00\x06\x00\x010\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x13\x00\x00\x01\x00\t\x00')
print('Yeah, you got the flag')

