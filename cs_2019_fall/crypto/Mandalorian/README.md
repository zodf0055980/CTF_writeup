## Mandalorian
這題就是要去解給後面 4 bit 的 LSB Oracle Attack
### 方法一
透過修改助教的 writeup
透過傳過去各自的 `pow(16,e,n) ^ n * c` 所回傳的數值，去存在 b 的 list，並透過 lsb 去找上下界，但解出來會有誤差，最後一個 char 會跑掉。之後果斷自己刻個方法二。

## 方法二
這裡的難點在要去取 `(16^-n)^e * c`，這裡如果直接用 pow 解會都變成 0，所以要帶換掉。先把式子變成 `(16^-1)^(n * e) * c` ，而這邊的 (16^-1) 可以直接用 Modular inverse 換掉，因為換掉後再去對 n 做 mod 值還是會相同。
Modular inverse 程式碼取自 : https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
之後一樣用 Modular inverse，並以此找出每 4 個 bit 的值，就能解出來啦。
