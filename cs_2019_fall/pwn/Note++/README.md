## Note++
原本找不到洞，發現 `read_input( char *buf , unsigned int size)` 對於傳過來的 size 會轉成 unsigned int...,這洞也太小了八....。
因此可以 `malloc(0)` 並 `read_input( notes[i].data , -1 );` 去達成 heap overflow。
原本想要去改 got 為 system 發現這題是 FULL RELRO，GOT 不可寫，因此只好蓋 `__malloc_hook`
透過 先 malloc(0) 再 malloc(0x58) 兩次，先透過大小為 0x20 的 chunk 去把 0x61 大小蓋成 0xc1 ，剛好是兩個 chuck，之後再 free 第一個 chunk，由於大小被我蓋成 0xc1 > 0x90，因此被 free 掉會被丟到 Unsorted bin 中，因此就可以 leak libc 位置。
之後可以透過把 free 掉 malloc(0x68) 的 chunk 的 fd 給 overflow 成 `l.sym.__malloc_hook - 0x10 -3` ，因此只要 malloc 兩次 0x68 大小，第二次就會拿到更改 `__malloc_hook` 的 fake chunk。
接下來把 `__malloc_hook` 蓋成 onegadget，但發現每個 onegadget 都不能用....
想到由於前面把 chunksize 便大，如果 free 掉會產生 `double free or corruption`，而其中得判斷會有 `__malloc_hook` ，就能 get shell。
