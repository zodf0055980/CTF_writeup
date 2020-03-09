# babystack
可以透過 strncmp 結合 overflow 去爆破 canary 的值。因為他 canary 是從 /dev/urandom 拿出來的。所以第一位不是 0 byte。
並可以再往下爆破到 save rbp，去拿到 pie 位置。

但最重要的是拿到 libc addr ，copy 可以蓋掉 stack 上的值，我們可以把 stack 上殘留的值給蓋到比較的地方再去暴力解出 libc addr (libc 2.27 是蓋不到的但 2.23 給你，害我卡超久.....)

之後在用 copy 把 save rip 蓋成 onegadget 就好了。
因為要暴力解，連線也太久了八......。
