# warngame
## 第一題
裡面有給暗藏的 phpinfo，透過他找到 sess_ 的儲存目錄，再用 LFI 存取。

## 第二題
.git 洩漏拿到密碼，再改 cookie

## 第三題
首先先用 LFI 找 etc/passwd 在哪一層目錄，再用 soft link (symbolic link) `ln -s 目標 建立檔案` 去給他 flag 位置並用壓縮檔包起來上傳就好了

## LoginTest
nosql injection

## sqltest
待解
