## Cathub_Party
首先先註冊一個帳號，他會把加密過得東西放在 cookies
```
FLAG = 'Jtm8jk83Ae72fNaR4HviRBySPZupVeLNCKO9uj3zZwlsxHriQeWp0UcLQpNpSn3oJSrolxfYlv4dGe7ssH8I4OeKRR7gqMAAZ0fhiznFpXNkSs2ZqdrvFJqAVdCs9BHb'
PHPSESSID = 'jnotfbc608o1sjaenh08b0adsa'
racksession = 'BAh7CEkiD3Nlc3Npb25faWQGOgZFVEkiRTU0YTdjOWNmZDcyYzMxMTI0ODQw%0AMzg3N2I4MzEzZmY3YjI4NWYxM2I3NmJjYjZlY2NlODA4ZTgzYjM2Njg4YzQG%0AOwBGSSIKZmxhc2gGOwBGewBJIgx1c2VyX2lkBjsARmkh%0A--815b7a00734fa9026e446dfb9773cb31fa8e5664'
```
首先先把 FLAG 解碼，感覺就是簡單的 base64。先解密，然後自己寫一個腳本去暴力解 Padding Oracle Attack。透過 cookie 傳給網站，並看他回傳的值，如果有 `CHEATER!!!` 代表傳送的東西不符合 CBC 的格式。
先試試 block size 是 8 的，發現 padding > 8，發現他的大小不是 8 ，最後測出來 block size 是 16 。
在解倒數第二段的明文時發現會一直送失敗，之後發現少一個 block 會使 base64 後數值有 `=` ，因此要做 quote()。
原本要用網路上的範例，但發覺好難用，效法 jserv 的精神，自己刻一個。
會發現解到中途會有一個明文解不出來，之後發現是 `F`，把 `F` 加上去就是 flag 了。
code : 隨便寫的所以有些地方寫很醜
