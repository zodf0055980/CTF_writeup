#include <stdio.h>
#include <stdlib.h>

char buf_bss[100];

int main(){
	setbuf(stdin, 0);
	setbuf(stdout, 0);
	setbuf(stderr, 0);
	char buf[30];
	puts("Who are you>");
	gets(buf_bss);
	puts("What do you want>");
	gets(buf);
	puts("bye ~");
	return 0;
}