#include <stdio.h>
#include <stdlib.h>

int main(){
	setbuf(stdin, 0);
	setbuf(stdout, 0);
	setbuf(stderr, 0);
	char buffer[200];
	puts("##############################");
	puts("Hello~~");
	printf("buffer address: 0x%lx\n", buffer);
	puts("##############################");
	puts("Input:");
	gets(buffer);
	puts(buffer);
	puts("bye~");
}