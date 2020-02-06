#解答
```
gdb-peda$ info frame
Stack level 0, frame at 0xffffd010:
 eip = 0x804869a in magic; saved eip = 0x65414149
 called by frame at 0xffffd014
 Arglist at 0xffffd008, args: 
 Locals at 0xffffd008, Previous frame's sp is 0xffffd010
 Saved registers:
  ebp at 0xffffd008, eip at 0xffffd00c
gdb-peda$ pattern offset 0x65414149
1698775369 found at offset: 72
```
32位元 看eip
為了過後面的 strlen
改成前面有個 /x00 
位置由於 scanf 會把 0x0804860d 中的 0d 吃掉
所以改下面的位置
