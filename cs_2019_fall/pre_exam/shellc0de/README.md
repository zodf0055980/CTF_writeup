## PWN
我覺的是最難的一題，因為一開始有使用 `read( 0 , shellcode , 0x100 );` 所以 plt 會有 read_plt ，因此我去 call readplt 去執行第二次 read() 而第二次 read 的東西不會經過字元檢查，因此就可以隨意給 shellcode 了。
其中因為遠端檔案有開 ASLR，而對於位置的末 3 個 bytes 不會變動，而其他的 bytes 會變動，因此透過 pop 上一個 function 所存的位置，透過 bitwise 的操作去取得 readplt 的位置和執行 function 的位置。
R10 為 read_plt 位置
R14 為 執行 `void (*hello)() = shellcode;` 的位置
