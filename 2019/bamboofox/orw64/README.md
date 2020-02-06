# 解答
%rax | System call | %rdi |  %rsi | %rdx
--- | --- | --- | --- | ---
0 | sys_read | unsigned | int fd | char *buf	size_t count
1 | sys_write | unsigned | int fd | const char *buf	size_t count		
2 | sys_open | const char *filename | int flags	| int mode	

Read :
rdx = length 要用長一點
rsi = addr to buffer = open 的  rsp
rdi = fd = open 回傳 rax

Write ：
寫到螢幕上
rdi = STDOUT_FILENO = 1
rsi = 不變
rdx = length = read 回傳的 rax

要求null-free(攻擊字串間不能夠有\x00)

把 shellcode 轉 hex
https://defuse.ca/online-x86-assembler.htm

shellcode c 程式
gcc -z execstack -o shell shell.c
