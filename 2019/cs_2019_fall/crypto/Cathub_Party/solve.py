import base64
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

error = 'CHEATER!!!'
my_FLAG = 'Jtm8jk83Ae72fNaR4HviRBySPZupVeLNCKO9uj3zZwlsxHriQeWp0UcLQpNpSn3oJSrolxfYlv4dGe7ssH8I4OeKRR7gqMAAZ0fhiznFpXNkSs2ZqdrvFJqAVdCs9BHb'
my_PHPSESSID = 'jnotfbc608o1sjaenh08b0adsa'
my_racksession = 'BAh7CEkiD3Nlc3Npb25faWQGOgZFVEkiRTU0YTdjOWNmZDcyYzMxMTI0ODQw%0AMzg3N2I4MzEzZmY3YjI4NWYxM2I3NmJjYjZlY2NlODA4ZTgzYjM2Njg4YzQG%0AOwBGSSIKZmxhc2gGOwBGewBJIgx1c2VyX2lkBjsARmkh%0A--815b7a00734fa9026e446dfb9773cb31fa8e5664'

def  test(cut , c):
    ch = b''
    for i in range(6-c):
        ch += cut[i]
    data = quote(base64.b64encode(ch).decode("utf-8"))
    my_cookies = {'FLAG':data,'PHPSESSID':my_PHPSESSID,'rack.session':my_racksession}
    r = requests.get("https://edu-ctf.csie.org:10190/party.php", cookies = my_cookies , verify = False)
    found = False
    if ( r.text.find(error) < 0 ):
        found = True
    return found
flag = [ [] , [] ,[] , [] , [] ,[] ]
data = base64.b64decode(my_FLAG)
cut = []
do_end = False
for i in range(6):
    first = i*16
    cut.append(data[first:first+16])
print(cut)

for i in range(5): #5
    j = 16
    xor_n = [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ]
    
    while( j != 0 ):
        decode = cut.copy()
        if( do_end == True ):
            li  = list(decode[4-i])
            for k in range(j , 16):
                # print('xor = ', xor_n[k] ^ (17 - j) )
                li[ k] = li[ k] ^ (xor_n[k] ^ (17 - j) )
            decode[4-i] = b''.join( bytes([d]) for d in li )

        for k in range(1,256):
            send = decode.copy()
            l = list(send[4-i])
            l[ j - 1 ] = l[ j - 1 ] ^ k
            send[4-i] = b''.join( bytes([d]) for d in l )
            re = test(send,i)
            if(re == True):
                end = k ^ (17 - j)
                if( do_end == False ):
                    do_end = True
                    j -= end
                    for c in range(end):
                        xor_n[ 15 - c ] = end
                else :
                    xor_n[ j - 1  ] = end
                    j -= 1
                break
            if(k == 255):
                flag[5-i] = xor_n
                e = ''
                for i in range(len(flag)):
                    e += ''.join(chr(z) for z in flag[i])
                print('end_flag = ',e)
                exit(0)
        print(xor_n)
    flag[5-i] = xor_n
    print('flag = ',flag)