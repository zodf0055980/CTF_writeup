#!/usr/bin/python -u
import random,string

encflag = "BNZQ:KLRXRNLXL{1_W8FF0Y_t0ic7l9_m5p_ruKo_vbjUOH}"
flag = ""
random.seed("random")
for c in encflag:
  if c.islower():
    #rotate number around alphabet a random amount
    flag += chr((ord(c)-ord('a')-random.randrange(0,26))%26 + ord('a'))
  elif c.isupper():
    flag += chr((ord(c)-ord('A')-random.randrange(0,26))%26 + ord('A'))
  elif c.isdigit():
    flag += chr((ord(c)-ord('0')-random.randrange(0,10))%10 + ord('0'))
  else:
    flag += c
print flag

