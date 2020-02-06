## EDU 2019 election
### leak
恩..是不是出錯週啦，這題沒有用到 heap，但是保護機制是全開的....
首先先想辦法 leak，發現在這裡
```
char buf[0xc8];
char token[0xb8] = {0};

int len = read( 0 , buf , sizeof( buf ) );
if( memcmp( buf , token , len ) ){
    puts( "Invalid token." );
    break;
}
```
發現我們可以去透過輸入 buf 去暴力破解 2 個 byte，分別為 canary 和 rbp。
去嘗試把 token 設為 'a' * 0xb8 並輸入 'a' * 0xb8 + '\0' 發現是成功的，證實我的想法，因此就可以寫個迴圈去爆破他。
由於 rbp 所存的值為 `__libc_csu_init`，因此可以藉此去拿到 pie base。且每次執行時 pie 都是相同的。
之後在 `read( 0 , msg , candidates[idx].votes );` 且 votes 為 uint8_t ，最大可為 255。 且 `char msg[0xe0];`，
但發現 stack 在 msg 後還有 1 個 byte 被用來做其他事情。
因此可以蓋 23 個 char。
而 cannary + save rbp 為 16，發現無法完全蓋滿 save rip。但由於是 little endian，所以只要蓋部份的 code 即可。
因此就能透過 buf 去做 Stack pivoting 達成 rop。
### rop
可以透過 return to plt 去達成 leak libc base，並把 rbp 指到一個可寫段。
但後續原本想要跳 main 但在 main 會執行失敗。
想到透過 rop 串 read 對 buf 寫入，但是因為沒有對 rdi 操作，因此 read 會失敗。但也找不到 pop rdi 的 rop。
透過 ret2csu 去操控 rdi，寫入 one_gadget 的位置就能拿到 shell 了。
