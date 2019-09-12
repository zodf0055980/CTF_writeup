# 解法
他要求要得到 shell ，發現可以去把 printf 的 got 改成 system，之後在 program() 中輸入 /bin/sh 發現可以得到 system("/bin/sh");
在 gdb 中輸入 `readelf`
```
gdb-peda$ readelf 
.interp = 0x8048154
.note.ABI-tag = 0x8048168
.note.gnu.build-id = 0x8048188
.gnu.hash = 0x80481ac
.dynsym = 0x80481d8
.dynstr = 0x8048318
.gnu.version = 0x8048402
.gnu.version_r = 0x804842c
.rel.dyn = 0x804847c
.rel.plt = 0x8048494
.init = 0x8048514
.plt = 0x8048540
.text = 0x8048650
.fini = 0x8048b64
.rodata = 0x8048b78
.eh_frame_hdr = 0x8048e00
.eh_frame = 0x8048e54
.init_array = 0x8049f08
.fini_array = 0x8049f0c
.jcr = 0x8049f10
.dynamic = 0x8049f14
.got = 0x8049ffc
.got.plt = 0x804a000
.data = 0x804a04c
.bss = 0x804a060
```
可以得到 .got = 0x8049ffc 
再使用 telescope
```
gdb-peda$ telescope 0x8049ffc 30
Warning: not running
0000| 0x8049ffc --> 0x0 
0004| 0x804a000 --> 0x8049f14 --> 0x1 
0008| 0x804a004 --> 0x0 
0012| 0x804a008 --> 0x0 
0016| 0x804a00c --> 0x8048556 (<printf@plt+6>:	push   0x0)
0020| 0x804a010 --> 0x8048566 (<__isoc99_fscanf@plt+6>:	push   0x8)
0024| 0x804a014 --> 0x8048576 (<fflush@plt+6>:	push   0x10)
0028| 0x804a018 --> 0x8048586 (<getchar@plt+6>:	push   0x18)
0032| 0x804a01c --> 0x8048596 (<fgets@plt+6>:	push   0x20)
0036| 0x804a020 --> 0x80485a6 (<__stack_chk_fail@plt+6>:	push   0x28)
0040| 0x804a024 --> 0x80485b6 (<puts@plt+6>:	push   0x30)
0044| 0x804a028 --> 0x80485c6 (<system@plt+6>:	push   0x38)
0048| 0x804a02c --> 0x80485d6 (<__gmon_start__@plt+6>:	push   0x40)
0052| 0x804a030 --> 0x80485e6 (<exit@plt+6>:	push   0x48)
0056| 0x804a034 --> 0x80485f6 (<strlen@plt+6>:	push   0x50)
0060| 0x804a038 --> 0x8048606 (<__libc_start_main@plt+6>:	push   0x58)
0064| 0x804a03c --> 0x8048616 (<fopen@plt+6>:	push   0x60)
0068| 0x804a040 --> 0x8048626 (<memset@plt+6>:	push   0x68)
0072| 0x804a044 --> 0x8048636 (<putchar@plt+6>:	push   0x70)
0076| 0x804a048 --> 0x8048646 (<__isoc99_scanf@plt+6>:	push   0x78)
0080| 0x804a04c --> 0x0 
0084| 0x804a050 --> 0x0 
```
比起之前用 objdump 拿 got 簡單很多
