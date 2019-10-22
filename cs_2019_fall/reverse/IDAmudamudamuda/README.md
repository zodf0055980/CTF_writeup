# HW2
contributed by <0856162 吳宗遠>
###### tags: `cs2019`

看到 binary 檔，首先 ida 先開起來，找到有 print 字串的位置。
![](https://i.imgur.com/Qq2Ack2.png)
首先先進入 sub_401000 ，判斷是在做 windows 前處理
把它給的資訊做命名一下
![](https://i.imgur.com/Xw0vHuP.png)
![](https://i.imgur.com/rxoKj4r.png)
舒服多了....

再來打開 sub_401070 判斷是把 .data 的值加上 seed，之後用 X64dbg 動態執行也證實是把 .data 的值加上 seed。
之後看 sub_401270
![](https://i.imgur.com/wcUsjFT.png)
他是把 .data 中的值拿來當 function 執行，因此跑去看他的 function
![](https://i.imgur.com/Z01Z7aC.png)
照他的提示有說要去懂 function 的呼叫 (一開始想說可能是用 syscall 去 write 到螢幕，結果不是......)
在執行新的 function 時，首先要去 push ebp, mov ebp,esp ，先利用方便的[組譯網站](https://defuse.ca/online-x86-assembler.htm#disassembly) 去轉成 strings
```
0:  55                      push   ebp
1:  89 e5                   mov    ebp,esp
```
發現 seed 為 16。
之後改用 x64dbg 動態執行，執行到 .data 的 function 上。
發現他把輸入讀出來，做 
```
0130002C | 83C1 23                  | add ecx,23                              |
0130002F | 83F1 66                  | xor ecx,66                              |
```
並和 ebp-4 上的值做比較，去找到當時的 ebp-4 位置
![](https://i.imgur.com/lFkjEwL.png)
把他的值取出來，寫程式運算，我寫一個簡單的 C
```clike
#include<stdio.h>

int main(){
    int cmp[] = {0x0F,0x09,0x02,0x0C,0xF8,0xFA,0x30,0xF0,0x22,0x22,0xFA,0x30,0xF0,0x22,0x22,0xFA,0x30,0xF0,0x22,0x22,0x35,0xED,0xE4,0xF6,0xFA,0xE4,0xEC,0x35,0xE1,0x22,0x22,0xC6};

    int i;
    for(i = 0 ;i < 32 ; i++ ) {
        printf("%c", (cmp[i] ^ 0x66) - 0x23 );
    }
    return 0;
}
```
flag 就出來啦
FLAG{y3s!!y3s!!y3s!!0h_my_g0d!!}
