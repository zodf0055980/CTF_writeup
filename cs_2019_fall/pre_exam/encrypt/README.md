## Crypto
只有 op3,op4 要逆傳回去要先重寫 code，其他皆為對稱加密，因此可以透過 python 的 index 去找出 op3，op4 逆轉的表格，就能寫逆轉的程式碼。
而我沒有實做 `for i in map(int, f'{key:08b}'):`的逆轉，因為最後要猜 key，逆轉回去會沒有效果。

