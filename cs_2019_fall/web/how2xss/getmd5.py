from Crypto.Hash import MD5

i = 0
while(1):
    h = MD5.new()
    h.update('kaibro' + str(i))
    res = h.hexdigest()[:5]
    if( res == "7ee49") :
        print i
        break
    i = i + 1
