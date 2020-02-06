# Hashpump

```
yuan@yuan-All-Series:~/HashPump$ ./hashpump 
Input Signature: 9863bb3cecccfdb82f689e2ddbdcd9c7ea3c069eb73a730d149c3aae2d60b7c0
Input Data: user=someone
Input Key Length: 44
Input Data to Add: user=admin
e43ae12ce0024abef5a376eebfc2ac7fc5a73d6be3a4b871f203f53e12191b5c
user=someone\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc0user=admin
```

```
yuan@yuan-All-Series:~$ python
Python 2.7.15+ (default, Nov 27 2018, 23:36:35) 
[GCC 7.3.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import base64
>>> s= "user=someone\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc0user=admin"
>>> a = base64.b64encode(s)
>>> print a
dXNlcj1zb21lb25lgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHAdXNlcj1hZG1pbg==
```
```
input your token: dXNlcj1zb21lb25lgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHAdXNlcj1hZG1pbg==
input your authentication code: e43ae12ce0024abef5a376eebfc2ac7fc5a73d6be3a4b871f203f53e12191b5c
```

