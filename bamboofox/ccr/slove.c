#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>
#define SIZE 40
int hash[36] = {405, 434, 457, 506, 467, 449, 465, 398, 381, 459, 465, 466, 538, 542, 546, 467, 449, 453, 463, 448, 523, 457, 448, 442, 455, 452, 521, 536, 463, 460, 467, 466, 453, 467, 483, 372};

int main()
{
    char s[40];
    memset(s,0,40);
    s[0] = 'F';
    s[1] = 'L';
    s[2] = 'A';
    s[3] = 'G';
    int temp = s[0] + s[1] + s[2] +s[3];
    int i;
    for ( i = 0; i < 36; i ++) {
        s[i + 4] = hash[i] - temp;
        temp = temp - s[i] + s[i+4];
    }
    printf("%s\n",s);
}

