#include <stdio.h>

#define true 1
#define false 0
#define WHITE_COLOR 65535
#define BLACK_COLOR 0
#define RED_COLOR 63488
#define GREEN_COLOR 2020
#define BLUE_COLOR 31

typedef unsigned short color_t;
typedef int bool;

typedef struct Gamestate {
  int x;
  int y;
  char draw_mode;
  bool is_drawing;
} Gamestate;

typedef struct RectState {
  int start_x;
  int start_y;
  int end_x;
  int end_y;
} RectState;

void init_graphics();
void exit_graphics();
void sleep_ms(long ms);
void clear_screen();
char getkey();
void draw_pixel(int, int, color_t);
void draw_rect(int x1, int y1, int width, int height, color_t c);

RectState current_rect;

void draw_rect_from_state(RectState state, color_t color) {
  int width = state.end_x - state.start_x;
  int height = state.end_y - state.start_y;
  draw_rect(state.start_x, state.start_y, width, height, color);
}

void draw_frame(Gamestate state, Gamestate last_state) {
  int x = state.x;
  int y = state.y;

  // If we're in "pencil" mode, just draw pixels
  if (state.is_drawing && state.draw_mode == 'p') {
    draw_pixel(x, y, WHITE_COLOR);
  }

  // If we're in "rectangle" model, draw a rectangle
  if (state.is_drawing && state.draw_mode == 'r') {
    // If we're starting a new shape, initialize the current rectangle holder
    if (!last_state.is_drawing) {
      current_rect.start_x = x;
      current_rect.start_y = y;
    }
    // If we're not drawing a new shape, remove the old shape
    if (last_state.is_drawing)
      draw_rect_from_state(current_rect, BLACK_COLOR);

    // Draw the shape as it currently is
    current_rect.end_x = x;
    current_rect.end_y = y;
    draw_rect_from_state(current_rect, WHITE_COLOR);
  }

  // If we're not drawing, mode a little red dot around to show where the "cursor" is
  if (state.draw_mode == '\0') {
    if (last_state.draw_mode == '\0')
      draw_pixel(last_state.x, last_state.y, BLACK_COLOR);
    draw_pixel(x, y, RED_COLOR);
  }
}

int main(int argc, char** argv) {
  // Initialization
  init_graphics();
  clear_screen();
  Gamestate current_state, last_state;
  current_state.x = 0;
  current_state.y = 0;
  current_state.draw_mode = '\0';
  current_state.is_drawing = false;
  last_state.x = 0;
  last_state.y = 0;
  last_state.draw_mode = '\0';
  last_state.is_drawing = false;
  char input;

  // Game loop
  do {
    input = getkey();
    if (input == 'h')
      current_state.x -= 1;
    else if (input == 'l')
      current_state.x += 1;
    else if (input == 'j')
      current_state.y += 1;
    else if (input == 'k')
      current_state.y -= 1;
    else if (input == 'p' || input == 'r') {
      if (input == current_state.draw_mode) {
        current_state.draw_mode = '\0';
        current_state.is_drawing = false;
      } else if (last_state.draw_mode == '\0') {
        current_state.draw_mode = input;
        current_state.is_drawing = true;
      }
    }
    draw_frame(current_state, last_state);
    last_state = current_state;
    sleep_ms(10);
  } while (input != 'q');

  exit_graphics();
  return 0;
}
