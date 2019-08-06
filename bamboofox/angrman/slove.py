# $ mkvirtualenv angr
# $ pip install angr
# $ pip install pwn

import angr
from pwn import *

# pro = process("angrman")
# ag = angr.Project("./angrman")
# pa = ag.factory.path_group().explore(find=0x400d2b)
# res = pa.found[0].state.posix.dumps(0)
# pro.send(res)

# print pro.recvall()
# print res

pro = process("angrman")
p = angr.Project('./angrman', load_options={"auto_load_libs": False})
ex = p.surveyors.Explorer(find=(0x400d2b))
ex.run()
res =  ex.found[0].state.posix.dumps(0)
pro.send(res)

print pro.recvall()
print  res