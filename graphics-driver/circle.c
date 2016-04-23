#define GREEN_COLOR 2020

typedef unsigned short color_t;

void init_graphics();
void exit_graphics();
void clear_screen();
void fill_circle(int x, int y, int r, color_t c);

int main(int argc, char** argv) {
  init_graphics();
  clear_screen();

  int x, y;
  fill_circle(120, 120, 100, GREEN_COLOR);

  exit_graphics();
  return 0;
}
