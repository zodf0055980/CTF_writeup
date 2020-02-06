```
Give you a chance to find the flag: ls -al
total 92
drwxr-xr-x   1 root root 4096 Feb  4 23:57 .
drwxr-xr-x   1 root root 4096 Feb  4 23:57 ..
-rwxr-xr-x   1 root root    0 Feb  4 23:57 .dockerenv
drwxr-xr-x   1 root root 4096 Feb  4 15:54 bin
drwxr-xr-x   2 root root 4096 Apr 24  2018 boot
drwxr-xr-x   5 root root  340 Feb  4 23:57 dev
drwxr-xr-x   1 root root 4096 Feb  4 23:57 etc
-r--------   1 root root   28 Feb  4 17:03 flag
drwxr-xr-x   1 root root 4096 Feb  4 17:03 home
drwxr-xr-x   1 root root 4096 May 23  2017 lib
drwxr-xr-x   2 root root 4096 Dec  2 12:43 lib64
drwxr-xr-x   2 root root 4096 Dec  2 12:43 media
drwxr-xr-x   2 root root 4096 Dec  2 12:43 mnt
drwxr-xr-x   2 root root 4096 Dec  2 12:43 opt
dr-xr-xr-x 842 root root    0 Feb  4 23:57 proc
-rwsr-xr-x   1 root root 8488 Feb  4 17:03 readflag
-rw-r--r--   1 root root  227 Feb  4 17:03 readflag.c
drwx------   1 root root 4096 Feb  5 00:48 root
drwxrwxr--   1 root root 4096 Dec 19 04:21 run
drwxr-xr-x   1 root root 4096 Feb  4 15:54 sbin
drwxr-xr-x   2 root root 4096 Dec  2 12:43 srv
dr-xr-xr-x  13 root root    0 Feb  4 09:17 sys
drwx-wx-wt   1 root root 4096 Feb  6 13:45 tmp
drwxr-xr-x   1 root root 4096 Dec  2 12:43 usr
drwxr-xr-x   1 root root 4096 Dec  2 12:43 var
```

```
#include <stdio.h>
#include <stdlib.h>

int main()
{
    FILE *f;
    char flag[0x100];
    char buf[0x100];

    f = fopen("/flag", "r");
    fgets(flag, 0xff, f);
    fgets(buf, 0xff, stdin);
    printf(buf);

    return 0;
}

```
