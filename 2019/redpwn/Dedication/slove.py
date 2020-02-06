import numpy as np
from PIL import Image
import random
import string
import glob
png = glob.glob("*.png")[0]
f = open(png,"r").read()

w = 400
h = 600

tex = "["

for i in range(len(f)):
        if(f[i] == '(' ) :
                tex = tex + '['
        elif(f[i] == ')') :
                tex = tex + ']'
        elif(f[i] == ' ' ) :
                tex = tex + ','
        else :
                tex = tex + f[i]

tex = tex + ']'
print tex
p = eval(tex)
print len(p)
arr = np.zeros([h,w,3])
k = 0
for i in range(h):
     for j in range(w):
        arr[i][j] = p [k]
        k = k+1
img = Image.fromarray(np.uint8(arr))
img.save("flag.png")
