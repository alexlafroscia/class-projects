/**
 * Trafficsim.c
 * Author: Alex LaFroscia
 * Date: Oct 11, 2015
 */

#define SIZE_OF_QUEUE 100
#define CONSUMER_SLEEP_SECONDS 2
#define PRODUCER_SLEEP_SECONDS 20

// Colors to use for printing the different threads
#define KRED  "\x1B[31m"
#define KGRN  "\x1B[32m"
#define KBLU  "\x1B[34m"

#include <sys/mman.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <linux/unistd.h>

struct cs1550_task_queue
{
  int in;
  int out;
  struct task_struct* tasks;
};

struct cs1550_sem
{
  int value;
  struct cs1550_task_queue queue;
};

typedef enum Direction
{
  NORTH = 0,
  SOUTH = 1
} Direction;

typedef struct Car {
  int num;     // ID number for the car
} Car;

struct car_queue {
  int in;      // Track index to "push" to
  int out;     // Track index to "pop" from
  int count;   // Keep track of count, for consumer use
  Car* cars;   // Array of cars
};

struct cs1550_sem *total_num_cars;
struct cs1550_sem *south_mutex;
struct cs1550_sem *north_mutex;

void down(struct cs1550_sem *sem)
{
  syscall(__NR_cs1550_down, sem);
  if (sem == total_num_cars)
  {
    printf("Value of Total Car semaphore is: %d\n", sem->value);
  }
}

void up(struct cs1550_sem *sem)
{
  syscall(__NR_cs1550_up, sem);
  if (sem == total_num_cars)
  {
    printf("Value of Total Car semaphore is: %d\n", sem->value);
  }
}

int check_producer_should_sleep()
{
  int num = rand() % 10;
  return num > 8;
}

// Output shown in Red
void north_producer(struct car_queue *queue)
{
  int north_id = 1;
  srand(time(NULL) ^ (getpid()<<16));
  while (1)
  {
    down(north_mutex);

    // Put a car in the north queue
    Car next_car;
    next_car.num = north_id++;

    // Put a car in the North queue
    queue->cars[queue->in] = next_car;
    queue->in = (queue->in + 1) % SIZE_OF_QUEUE;
    queue->count++;
    //printf("%s%d cars in the North queue\n", KRED, queue->count);

    up(north_mutex);
    up(total_num_cars);

    // Sleep 20% of the time
    if (check_producer_should_sleep())
    {
      sleep(PRODUCER_SLEEP_SECONDS);
    }
  }
}

// Output shown in Blue
void south_producer(struct car_queue *queue)
{
  int south_id = 1;
  srand(time(NULL) ^ (getpid()<<16));
  while (1)
  {
    down(south_mutex);

    // Put a car in the south queue
    Car next_car;
    next_car.num = south_id++;
    queue->cars[queue->in] = next_car;
    queue->in = (queue->in + 1) % SIZE_OF_QUEUE;
    queue->count++;
    //printf("%s%d cars in the South queue\n", KBLU, queue->count);

    up(south_mutex);
    up(total_num_cars);

    // Sleep 20% of the time
    if (check_producer_should_sleep())
    {
      sleep(PRODUCER_SLEEP_SECONDS);
    }
  }
}

// Output shown in Green
void consumer(struct car_queue *north_queue, struct car_queue *south_queue)
{
  int last_picked_direction = NORTH;
  printf("%sInitializing the Consumer\n", KGRN);
  while (1)
  {
    down(total_num_cars);

    // Decide which direction to allow
    int allow_south;
    if (north_queue->count == 10)
    {
      allow_south = 0;
      printf("%sToo many cars to the North; must pick from there\n", KGRN);
    }
    else if (south_queue->count == 10)
    {
      allow_south = 1;
      printf("%sToo many cars to the South; must pick from there\n", KGRN);
    }
    else
    {
      // Convert last direction into next allowed direction based on enum values
      allow_south = last_picked_direction;
    }

    // Allow either the south or north queue to cross through
    if (allow_south && south_queue->in != south_queue->out)
    {
      last_picked_direction = SOUTH;
      down(south_mutex);

      Car next_car = south_queue->cars[south_queue->out];
      south_queue->out = (south_queue->out + 1) % SIZE_OF_QUEUE;
      south_queue->count--;
      printf("%sDequeued Car %d from the North\n", KGRN, next_car.num);

      sleep(CONSUMER_SLEEP_SECONDS);
      up(south_mutex);
    }
    else if (north_queue->in != north_queue->out)
    {
      last_picked_direction = NORTH;
      down(north_mutex);

      Car next_car = north_queue->cars[north_queue->out];
      north_queue->out = (north_queue->out + 1) % SIZE_OF_QUEUE;
      north_queue->count--;
      printf("%sDequeued Car %d from the South\n", KGRN, next_car.num);

      sleep(CONSUMER_SLEEP_SECONDS);
      up(north_mutex);
    }
  }
}

int main(int argc, char** argv)
{
  // Initialize values for semaphores
  total_num_cars = mmap(NULL, sizeof(struct cs1550_sem), PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, 0, 0);
  total_num_cars->value = 0;
  south_mutex = mmap(NULL, sizeof(struct cs1550_sem), PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, 0, 0);
  south_mutex->value = 1;
  north_mutex = mmap(NULL, sizeof(struct cs1550_sem), PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, 0, 0);
  north_mutex->value = 1;

  // Initialize queues of cars
  // Both the queue struct, which tracks the "in" and "out" pointers as well as the arrays
  // of cars themselves all need to be Heap-allocated, since all of the threads need to share
  // access to these data structures.
  int size = sizeof(Car) * SIZE_OF_QUEUE;
  struct car_queue *north_queue = mmap(NULL, sizeof(struct car_queue), PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, 0, 0);
  north_queue->cars = mmap(NULL, size, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, 0, 0);
  north_queue->in = 0;
  north_queue->out = 0;
  north_queue->count = 0;
  struct car_queue *south_queue = mmap(NULL, sizeof(struct car_queue), PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, 0, 0);
  south_queue->cars = mmap(NULL, size, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, 0, 0);
  south_queue->in = 0;
  south_queue->out = 0;
  south_queue->count = 0;

  // Fork the process twice, so that there are 3 threads total
  // 1. The "Consumer" thread
  // 2. The "North" producer thread
  // 3. The "South" producer thread
  if (fork() == 0) {
    consumer(north_queue, south_queue);
  } 
  if (fork() == 0) {
    north_producer(north_queue);
  } 
  south_producer(south_queue);
}

