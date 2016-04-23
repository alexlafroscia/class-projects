/*
 * Malloc and Free Project
 * Author: Alex LaFroscia
 * Date: Nov 1, 2014
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

#define MAX_MEM (1 << 30)
#define TWO_TO_THE(x) (1 << (x))
#define CURRENT_ROW_SIZE (1 << (index + 5))
#define SIZE_FROM_ORDER(order) (1 << (order + 5))


/*
 * Structs
 */
typedef struct FreeHeader {
  unsigned char used : 1;        // Amount of space allocated by this header
  struct FreeHeader *next;       // Link to the "next" FreeHeader
  struct FreeHeader *previous;   // Link to the "previous" FreeHeader
} FreeHeader;

typedef struct UsedHeader {
  unsigned char used : 1;        // Char for whether or not it is used
  unsigned int order : 7;                 // Order of allocation
                                 // Size = (1 << (order + 5))
} UsedHeader;

typedef struct TableRow {
  FreeHeader *next;              // Pointer to the first FreeHeader for this size
} TableRow;


/*
 * Function Prototpes
 */
FreeHeader* mcm_rec(int, int);
void mcm_free_rec(FreeHeader*, int);

/*
 * Global Variables
 */

// Global variable to hold the base address of the allocated space
// Initialized the first time that my_buddy_alloc is called
void * base;

// Table to hold all of the lists of allocated blocks
struct TableRow malloc_table[25] = { NULL };


/*
 * Functions
 */
void *my_buddy_malloc(int size)
{
  // If base is still null, run `mmap`, otherwise just move on and use the
  // previous value
  if (!base) {
    base = mmap(NULL, MAX_MEM, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANON, 0, 0);
  }

  // If malloc_table hasn't been created yet, set it up with a "row" for each
  // of the sizes.  Each row will represent blocks of size:
  //
  // (i + 1) * 32kb
  //
  // Which should make them easy to find
  if (!malloc_table[24].next) {
    *((FreeHeader*)base) = (FreeHeader){0, NULL, NULL};
    malloc_table[24].next = base;
  }

  int total_size = size + sizeof(FreeHeader);

  // Figure out the right order to use and start with
  int order;
  for(order = 0; order < 25; order++) {
    if (total_size < SIZE_FROM_ORDER(order))
      break;
  }

  void *address = mcm_rec(total_size, order);
  *((UsedHeader*)address) = (UsedHeader){1, order};
  return ((void *)address) + sizeof(UsedHeader);
}


void my_free(void *ptr)
{
  // Make a pointer to the UsedHeader for the deallocated memoery
  UsedHeader *header = (UsedHeader*)((void *)ptr - sizeof(UsedHeader));
  // Save the order off of it
  int order = header->order;
  // Replace the header with a FreeHeader
  *((FreeHeader*)header) = (FreeHeader){0, NULL, NULL};
  // Try to coallesce free space
  mcm_free_rec((FreeHeader*)header, order);
}


/*
 * Helper Functions
 * Functions used by my other functions to remove functionality from the main
 * programs and make them easier to read
 */

FreeHeader *mcm_rec(int size, int index)
{
  FreeHeader *header = malloc_table[index].next;
  if (header) {
    malloc_table[index].next  = header->next;
    return header;
  } else {
    // Get a new empty node from the previous order
    FreeHeader *empty = mcm_rec(size, index + 1);

    // Make the two new nodes
    *empty = (FreeHeader){0, (FreeHeader*)((void*)empty + SIZE_FROM_ORDER(index)), NULL};
    *(empty->next) = (FreeHeader){0, malloc_table[index].next, NULL};
    malloc_table[index].next = empty->next;
    return empty;
  }
}


void mcm_free_rec(FreeHeader *header, int order) {
  int size = SIZE_FROM_ORDER(order);
  int header_offset = (int)((void*)header - (void*)base);
  int buddy_offset = header_offset ^ size;
  FreeHeader *buddy = (FreeHeader*)((void*)base + buddy_offset);
  if (buddy->used || order == 24) {
    // Do this stuff if my buddy is not free
    header->next = malloc_table[order].next;
    header->next->previous = header;
    malloc_table[order].next = header;
  } else {
    // Do this stuff if my buddy is free
    // Coallesce!
    FreeHeader *pair = (header < buddy) ? header : buddy;
     if (header->previous) {
       header->previous->next = header->next;
     }
     if (header->next) {
       header->next->previous = header->previous;
     }
     if (buddy->previous) {
       buddy->previous->next = buddy->next;
     }
     if (buddy->next) {
       buddy->next->previous = buddy->previous;
     }
     if (!malloc_table[order].next->next) {
       malloc_table[order].next = NULL;
     }
    *pair = (FreeHeader){0, malloc_table[order + 1].next, NULL};

    if (malloc_table[order + 1].next) {
      malloc_table[order + 1].next->previous = pair;
    }

    if (malloc_table[order].next == malloc_table[order].next->next) {
      malloc_table[order].next = NULL;
    }
    malloc_table[order + 1].next = pair;
    mcm_free_rec(pair, order + 1);
  }
}

