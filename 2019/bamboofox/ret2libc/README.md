#解法
```
(base) yuan@yuan-All-Series:~/CTF_writeup/bamboofox/ret2libc$ objdump -T libc.so.6 | grep puts
00064da0 g    DF .text	000001a5  GLIBC_2.0   _IO_puts
00064da0  w   DF .text	000001a5  GLIBC_2.0   puts
000f1650 g    DF .text	00000408  GLIBC_2.0   putspent
000f2d80 g    DF .text	000001f1  GLIBC_2.10  putsgent
00063830  w   DF .text	00000145  GLIBC_2.0   fputs
00063830 g    DF .text	00000145  GLIBC_2.0   _IO_fputs
00068e00 g    DF .text	00000097  GLIBC_2.1   fputs_unlocked
(base) yuan@yuan-All-Series:~/CTF_writeup/bamboofox/ret2libc$ objdump -T libc.so.6 | grep system
00118dc0 g    DF .text	00000049  GLIBC_2.0   svcerr_systemerr
0003fe70 g    DF .text	00000038  GLIBC_PRIVATE __libc_system
0003fe70  w   DF .text	00000038  GLIBC_2.0   system
```
