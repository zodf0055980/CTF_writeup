#include<stdio.h>
#include<stdlib.h>
#include<string.h>

char name[32] = {0};
char secret[16] = {0};

void init(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    int fd = open("/dev/urandom", 0);
    if(fd < 0){
        printf("Error!!\n");
        exit(-1);
    }
    read(fd, secret, 16);
    close(fd);

}


int game(){
    char ans[16] = {0};
    int len = 0;
    int magic = 0;

    puts("Try my secret :");
    read(0, ans, 16);
    if(strncmp(ans, secret, strlen(ans))){
        puts("You don't know me :(");
        return 1;
    }

    puts("Give me a magic number :");
    scanf("%d", &magic);
    magic = abs(magic);
    if(2019 + magic < 2019 && 2019 - magic < 2019){
        puts("Passed!");
    }else{
        puts("You lose~");
        return 2;
    }

    return 0;
}

int main(){
    char message[1024] = {0};
    int size = 0;
    int result = 0;

    init();
    result = game();
    if(!result){
        puts("You win.");
        printf("Here is your reward : %p\n", printf);

        puts("Leave your name :");
        scanf("%16s", name);
        snprintf(message, 32, "Your name is : %s", name);

        puts("Winner can leave message at here :");
        puts("size :");
        scanf("%d", &size);

        if(size + 32 < 1024){
	    puts("Your message :");
	    read(0, message+32, size);
            puts("Good bye~");
        }else{
            puts("No! Message too long.");
        }
    }else{
        puts("Bye~");
    }

    return 0;
}
