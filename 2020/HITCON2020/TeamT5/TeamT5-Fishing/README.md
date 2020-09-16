# Team T5
flag 1 = `Flag{ TeamT5 - https://teamt5.org/}`
flag 2 = `Flag{TeamT5 - https://twitter.com/TeamT5_Official}
`
## flag
打開遊戲會是一個釣魚遊戲，並且有一個 inject.dll，因此猜測會是和該 dll 有相關。遊戲說明有提到分數要超過 555555，原本想要用 cheat engine 去更改遊戲內分數的，但想想還是用 reverse 解好了。

首先我使用 ghidra (因為電腦是 ubuntu 且沒有裝 wine，ida 開不起來)，就直接發現 inject.dll 中有個 function 叫 inject，直接看反組譯後的結果就看到 flag 了。
flag = `Flag{ TeamT5 - https://teamt5.org/}`
![](https://i.imgur.com/vzhcqXE.png)

看這個 function 的呼叫狀況發現會是在遊戲一開始會產生一個 thread 並隨時觀看分數的狀況，之後來解 hidden message。
# hidden message
可以看到 inject 一開始有呼叫到 FUN_10001010()，發現他內部是在做很簡單的加密，稍微把他美化一下整個 function 會長這樣
``` clike=
void FUN_10001010(void)

{
  int addr_count;
  undefined4 *add1;
  undefined4 *add2;
  uint xor_count;
  char unknown [26];
  char hidden [104];
  
  hidden[0] = '\x1c';
  hidden[1] = '$';
  hidden[2] = '<';
  hidden[3] = 'g';
  hidden[4] = 'k';
  hidden[5] = '\x06';
  hidden[6] = '*';
  hidden[7] = ',';
  hidden[8] = '\"';
  hidden[9] = '(';
  hidden[10] = '5';
  hidden[11] = 'k';
  hidden[12] = '\x12';
  hidden[13] = '$';
  hidden[14] = '>';
  hidden[15] = -0x57;
  hidden[16] = -0x35;
  hidden[17] = -0x2e;
  hidden[18] = '=';
  hidden[19] = '.';
  hidden[20] = 'k';
  hidden[21] = '8';
  hidden[22] = '>';
  hidden[23] = '(';
  hidden[24] = '(';
  hidden[25] = '.';
  hidden[26] = '.';
  hidden[27] = '/';
  hidden[28] = '.';
  hidden[29] = '/';
  hidden[30] = 'k';
  hidden[31] = '\"';
  hidden[32] = '%';
  hidden[33] = 'k';
  hidden[34] = '9';
  hidden[35] = '.';
  hidden[36] = '=';
  hidden[37] = '.';
  hidden[38] = '9';
  hidden[39] = '8';
  hidden[40] = '\"';
  hidden[41] = '%';
  hidden[42] = ',';
  hidden[43] = 'k';
  hidden[44] = '?';
  hidden[45] = '#';
  hidden[46] = '.';
  hidden[47] = 'k';
  hidden[48] = '\x0f';
  hidden[49] = '\a';
  hidden[50] = '\a';
  hidden[51] = 'e';
  hidden[52] = 'F';
  hidden[53] = 'A';
  hidden[54] = '\r';
  hidden[55] = '\'';
  hidden[56] = '*';
  hidden[57] = ',';
  hidden[58] = '0';
  hidden[59] = '\x1f';
  hidden[60] = '.';
  hidden[61] = '*';
  hidden[62] = '&';
  hidden[63] = '\x1f';
  hidden[64] = '~';
  hidden[65] = 'k';
  hidden[66] = 'f';
  hidden[67] = 'k';
  hidden[68] = '#';
  hidden[69] = '?';
  hidden[70] = '?';
  hidden[71] = ';';
  hidden[72] = '8';
  hidden[73] = 'q';
  hidden[74] = 'd';
  hidden[75] = 'd';
  hidden[76] = '?';
  hidden[77] = '<';
  hidden[78] = '\"';
  hidden[79] = '?';
  hidden[80] = '?';
  hidden[81] = '.';
  hidden[82] = '9';
  hidden[83] = 'e';
  hidden[84] = '(';
  hidden[85] = '$';
  hidden[86] = '&';
  hidden[87] = 'd';
  hidden[88] = '\x1f';
  hidden[89] = '.';
  hidden[90] = '*';
  hidden[91] = '&';
  hidden[92] = '\x1f';
  hidden[93] = '~';
  hidden[94] = '\x14';
  hidden[95] = '\x04';
  hidden[96] = '-';
  hidden[97] = '-';
  hidden[98] = '\"';
  hidden[99] = '(';
  hidden[100] = '\"';
  hidden[101] = '*';
  hidden[102] = '\'';
  hidden[103] = '6';
  addr_count = 0x1a;
  add1 = (undefined4 *)hidden;
  add2 = (undefined4 *)unknown;
  while (addr_count != 0) {
    addr_count = addr_count + -1;
    *add2 = *add1;
    add1 = add1 + 1;
    add2 = add2 + 1;
  }
  xor_count = 0;
  while (xor_count < 0x68) {
    unknown[xor_count] = unknown[xor_count] ^ 0x4b;
    xor_count = xor_count + 1;
  }
  OutputDebugStringA(hidden);
  FUN_100012b7();
  return;
}
```
可以看到程式一開始對整個 array 賦值，之後把 hidden array 前 26 個字複製到 unknown array 中，之後再把每個 array 做 xor，寫個簡單的 python 去解他。
```python=
hidden = [0x1c, 0x24, 0x3c, 0x67, 0x6b, 0x6, 0x2a, 0x2c, 0x22, 0x28, 0x35, 0x6b, 0x12, 0x24, 0x3e, 0xa9, 0xcb, 0xd2, 0x3d, 0x2e, 0x6b, 0x38, 0x3e, 0x28, 0x28, 0x2e, 0x2e, 0x2f, 0x2e, 0x2f, 0x6b, 0x22, 0x25, 0x6b, 0x39, 0x2e, 0x3d, 0x2e, 0x39, 0x38, 0x22, 0x25, 0x2c, 0x6b, 0x3f, 0x23, 0x2e, 0x6b, 0xf, 0x7, 0x7, 0x65,
          0x46, 0x41, 0xd, 0x27, 0x2a, 0x2c, 0x30, 0x1f, 0x2e, 0x2a, 0x26, 0x1f, 0x7e, 0x6b, 0x66, 0x6b, 0x23, 0x3f, 0x3f, 0x3b, 0x38, 0x71, 0x64, 0x64, 0x3f, 0x3c, 0x22, 0x3f, 0x3f, 0x2e, 0x39, 0x65, 0x28, 0x24, 0x26, 0x64, 0x1f, 0x2e, 0x2a, 0x26, 0x1f, 0x7e, 0x14, 0x4, 0x2d, 0x2d, 0x22, 0x28, 0x22, 0x2a, 0x27, 0x36, ]

hidden_message = "".join(chr(hidden[i] ^ 0x4b) for i in range(0x68))
print(hidden_message)
```
flag = `Flag{TeamT5 - https://twitter.com/TeamT5_Official}
`
