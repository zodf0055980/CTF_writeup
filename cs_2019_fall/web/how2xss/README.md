發現他有擋相同字元，所以先嘗試透過 <SVG/ONLoAD=alert(1)> 去產生 XSS。
由於直接使用 document.cookie 會被擋太多東西了，所以只能想辦法繞過他。
最後上網查到類似的解法，透過 `window.name` 和使用 `eval(name)` ，可以先在本機建一個網站
透過不同域 `window.name` 會不變的特性，可以把 cookie 傳出來。
由於在 `Report to admin` 中不會擋外部連結，直接傳自己的 index 給他就行了。
而 pow 就寫個簡單的 python 爆開即可
