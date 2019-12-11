## Casino++
這題目有開 NX，想要去 leak libc addr。
首先發現把 put got 改成 casino fuction 的位置，就可以無限的去修改想要的值。
之後想要 leak libc，因此去找可以去修改 rdi 的 function。發現有 `atoi` `srand` ，因此可以透過把這 `srand`  function got 改成 put_plt+6 ，並把 rdi 改成 `__libc_start_main` 的位置，就可以 leak 位置出來。
```
name =  'a' * 0x10 + p64(0x601ff0)
```
由於把 srand 改成 put_plt+6，所以前面更改的 put got 會回覆成 put 真正的位置，因此遇到很大的麻煩。
因為 `srand` 為 put_plt+6，而 put got 要改成 casino fuction 要更改兩次，但兩次後就會重新執行到 srand。因此我需要在剩下兩次的修改中 get shell。
原本想說把 got 改成 One gadget，但由於 `call` 會 push rdi，造成 `rsp` 無法對齊 `0x10`，movaps 會一直出錯。
原本想找找 libc 有沒有類似 `push [rsp]; ret` 的 gadget，但沒有....。
之後想到另一個沒有改到的 `atoi`，且修改的程式碼為
```
guess[idx] = read_int();
```
他會先執行 read_int 再更改到 got，所以不會出事。
因此把 atoi got 改成 system，輸入直接改 `/bin/sh` ，就拿到 shell 了。
