#include <fcntl.h>
#include <sys/mman.h>
#include <sys/ioctl.h>
#include <linux/fb.h>
#include <termios.h>
#include <time.h>
#include <unistd.h>
#include <sys/select.h>
#include "iso_font.h"

#define NUM_NS_IN_MS 1000000L;

typedef unsigned short color_t;

int framebuffer;
void* memo;
int size;
int screen_width;     // Screen width in pixels
int screen_height;    // Screen height in pixels
int bits_per_pixel;
struct termios term;

void init_graphics() {
  // Get the framebuffer
  framebuffer = open("/dev/fb0", O_RDWR);

  // Get the screen size
  struct fb_var_screeninfo var_info;
  ioctl(framebuffer, FBIOGET_VSCREENINFO, &var_info);
  screen_height = var_info.yres_virtual;
  bits_per_pixel = var_info.bits_per_pixel;

  struct fb_fix_screeninfo fix_info;
  ioctl(framebuffer, FBIOGET_FSCREENINFO, &fix_info);
  screen_width = fix_info.line_length * 8 / bits_per_pixel; // Bytes * bits / bits per pixel

  size = var_info.yres_virtual * fix_info.line_length;

  // Disable keyboard input
  ioctl(1, TCGETS, &term);
  term.c_lflag &= ~ICANON;
  term.c_lflag &= ~ECHO;

  ioctl(1, TCSETS, &term);

  // Make the memory map
  memo = mmap(0, size, PROT_READ|PROT_WRITE, MAP_SHARED, framebuffer, 0);
}

void exit_graphics() {
  munmap(memo, size);
  term.c_lflag |= ICANON;
  term.c_lflag |= ECHO;
  ioctl(1, TCSETS, &term);
  close(framebuffer);
}

void clear_screen() {
  const char clear_code[] = "\033[2J";
  write(STDOUT_FILENO, clear_code, 7);
}

char getkey() {
  // Set up to get which are ready to be read
  fd_set rfds;
  FD_ZERO(&rfds);
  FD_SET(0, &rfds);

  // Set the timeout so that we don't block at all
  struct timeval timeout;
  timeout.tv_sec = 0;
  timeout.tv_usec = 0;

  // Get the return value, or not
  int retVal = select(1, &rfds, NULL, NULL, &timeout);
  if (retVal != 1) {
    return '\0';
  }

  // If we got here, we're ready!
  char character;
  ssize_t size_read = read(STDIN_FILENO, &character, sizeof(char));
  return character;
}

void sleep_ms(long ms) {
  // Get number of seconds
  int seconds = 0;
  if (ms >= 1000)
    seconds = ms / 1000;

  // Get number of nanoseconds
  ms = ms % 1000;
  long ns = ms * NUM_NS_IN_MS;

  struct timespec req;
  req.tv_sec = seconds;
  req.tv_nsec = ns;
  nanosleep(&req, NULL);
}

void draw_pixel(int x, int y, color_t color) {
  // Make sure that we're not running larger than the board
  while (x <= 0)
    x += screen_width;
    x = x % screen_width;
  while (y <= 0)
    y += screen_height;
  y = y % screen_height;

  int index = y * screen_width;
  index = index + x;
  index = index * sizeof(color_t);

  // Set the pixel at the index to the given color
  *((color_t *)(memo + index)) = color;
}

void draw_rect(int x1, int y1, int width, int height, color_t c) {
  int x2 = x1 + width;
  int y2 = y1 + height;
  int i;
  for (i = x1; i < x2; i++) {
    draw_pixel(i, y1, c);
  }
  for (i = y1; i < y2; i++) {
    draw_pixel(x1, i, c);
    draw_pixel(x2, i, c);
  }
  for (i = x1; i < x2; i++) {
    draw_pixel(i, y2, c);
  }
}

void draw_fill_line(int from_x, int to_x, int to_y, color_t c) {
  while (abs(to_x - from_x) > 0) {
    draw_pixel(to_x, to_y, c);
    if (to_x > from_x) {
      to_x--;
    } else {
      to_x++;
    }
  }
  draw_pixel(from_x, to_y, c);
}

void fill_circle(int x0, int y0, int r, color_t c) {
  int x = r;
  int y = 0;
  int decision_over_2 = 1 - x;

  while (y <= x) {
    draw_fill_line(x0,  x + x0,  y + y0, c);
    draw_fill_line(x0,  y + x0,  x + y0, c);
    draw_fill_line(x0, -x + x0,  y + y0, c);
    draw_fill_line(x0, -y + x0,  x + y0, c);
    draw_fill_line(x0, -x + x0, -y + y0, c);
    draw_fill_line(x0, -y + x0, -x + y0, c);
    draw_fill_line(x0,  x + x0, -y + y0, c);
    draw_fill_line(x0,  y + x0, -x + y0, c);
    y++;
    if (decision_over_2 <= 0) {
      decision_over_2 += 2 * y + 1;   // Change in decision criterion for y -> y+1
    } else {
      x--;
      decision_over_2 += 2 * (y - x) + 1;   // Change for y -> y+1, x -> x-1
    }
  }
}

void draw_character(int x, int y, char character, color_t c) {
  int ascii = (int) character, i, j, current_x, current_y = y;
  ascii = ascii * 16;

  for (i = 0; i < 16; i++) {
    // Figure out what the first pixel location is
    int current_int = iso_font[ascii + i], mask = 128;
    current_x = x + 7;
    for (j = 0; j < 8; j++) {
      if (current_int & mask) {
        draw_pixel(current_x, current_y, c);
      }
      mask = mask >> 1;
      current_x--;
    }
    current_y++;
  }
}

void draw_text(int x, int y, const char *text, color_t c) {
  int counter = 0;
  char current_character = text[counter];

  while (current_character != '\0') {
    draw_character(x, y, current_character, c);
    current_character = text[++counter];
    x += 8;
  }
}
