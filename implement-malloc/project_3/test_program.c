#include <stdio.h>
#include "./mymalloc.h"

int main() {

  int *test = my_buddy_malloc(sizeof(int));
  *test = 5;

  int *test2 = my_buddy_malloc(sizeof(int));
  *test2 = 7;

  int *test3 = my_buddy_malloc(sizeof(int));
  *test3 = 10;

  printf("%d\n", *test);
  printf("%d\n", *test2);
  printf("%d\n", *test3);

  my_free(test);
  my_free(test2);
  my_free(test3);

  return 0;
}
