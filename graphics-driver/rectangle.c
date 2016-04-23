#define RED_COLOR 63488
#define BLUE_COLOR 31
#define NUM_COLS 6
#define NUM_ROWS 5
#define SQUARE_SIZE 60

typedef unsigned short color_t;

void init_graphics();
void exit_graphics();
void clear_screen();
void draw_rect(int x1, int y1, int width, int height, color_t c);

int main(int argc, char** argv) {
  init_graphics();
  clear_screen();

  int x, y;
  color_t color = RED_COLOR;
  for (x = 0; x < NUM_COLS; x++) {
    for (y = 0; y < NUM_ROWS; y++) {
      draw_rect(x * SQUARE_SIZE + x, y * SQUARE_SIZE + y, SQUARE_SIZE, SQUARE_SIZE, color);
      if (color == RED_COLOR)
        color = BLUE_COLOR;
      else
        color = RED_COLOR;
    }
  }

  exit_graphics();
  return 0;
}
