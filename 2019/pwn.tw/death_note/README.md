# Death Note
## printable shell code
網路上整理的 printable assembly
```
1.stack:
push/pop eax…
pusha/popa

2.math:
inc/dec eax…
sub al, 數字
sub byte ptr [eax… + 數字], al dl…
sub byte ptr [eax… + 數字], ah dh…
sub dword ptr [eax… + 數字], esi edi
sub word ptr [eax… + 數字], si di
sub al dl…, byte ptr [eax… + 數字]
sub ah dh…, byte ptr [eax… + 數字]
sub esi edi, dword ptr [eax… + 數字]
sub si di, word ptr [eax… + 數字]

3.logic:
and al, 數字
and dword ptr [eax… + 數字], esi edi
and word ptr [eax… + 數字], si di
and ah dh…, byte ptr [ecx edx… + 數字]
and esi edi, dword ptr [eax… + 數字]
and si di, word ptr [eax… + 數字]

xor al, 數字
xor byte ptr [eax… + 數字], al dl…
xor byte ptr [eax… + 數字], ah dh…
xor dword ptr [eax… + 數字], esi edi
xor word ptr [eax… + 數字], si di
xor al dl…, byte ptr [eax… + 數字]
xor ah dh…, byte ptr [eax… + 數字]
xor esi edi, dword ptr [eax… + 數字]
xor si di, word ptr [eax… + 數字]

4.cmp:
cmp al, 數字
cmp byte ptr [eax… + 數字], al dl…
cmp byte ptr [eax… + 數字], ah dh…
cmp dword ptr [eax… + 數字], esi edi
cmp word ptr [eax… + 數字], si di
cmp al dl…, byte ptr [eax… + 數字]
cmp ah dh…, byte ptr [eax… + 數字]
cmp esi edi, dword ptr [eax… + 數字]
cmp si di, word ptr [eax… + 數字]

5.轉移指令:
push 56h
pop eax
cmp al, 43h
jnz lable

<=> jmp lable

6.交換al, ah
push eax
xor ah, byte ptr [esp] // ah ^= al
xor byte ptr [esp], ah // al ^= ah
xor ah, byte ptr [esp] // ah ^= al
pop eax

7.清零:
push 44h
pop eax
sub al, 44h ; eax = 0

push esi
push esp
pop eax
xor [eax], esi ; esi = 0
```
index 可以給負值去蓋掉 got，之後就可以跑自己傳進去的 shellcode ，這題要求 printable assembly。
從 2.27 進去可以看到 edx 是 0x60 結尾。因此可以透過 ` sub    BYTE PTR [eax+數字], dl` 或是 `xor    BYTE PTR [eax+數字], dl` 對數字做更改就好。
之後本地端跑成功但遠端會失敗，換到 2.23 看才發現進去時的 edx 尾數是 0x08 結尾，透過 push 換掉即可成功。
