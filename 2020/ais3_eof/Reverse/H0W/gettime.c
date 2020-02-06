#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
  struct tm info;
  info.tm_year = 2019 - 1900;
  info.tm_mon = 8;
  info.tm_mday = 11;
  info.tm_hour = 5 + 8;
  info.tm_min = 25;
  info.tm_sec = 14;
  time_t ret = mktime(&info);
  printf("%ld\n", ret);
}
