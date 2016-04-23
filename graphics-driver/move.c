typedef unsigned short color_t;

#define WHITE_COLOR 65535

char getkey();
void clear_screen();
void draw_rect(int x1, int y1, int width, int height, color_t c);
void draw_text(int x, int y, const char* text, color_t c);
void exit_graphics();
void init_graphics();
void sleep_ms(long ms);

int main(int argc, char** argv)
{
  init_graphics();
  clear_screen();

  char key;
  int x = (640 - 20) / 2;
  int y = (480 - 20) / 2;

  draw_text(0, 16 * 0, "Controls:", WHITE_COLOR);
  draw_text(0, 16 * 1, "Up:    w", WHITE_COLOR);
  draw_text(0, 16 * 2, "Left:  a", WHITE_COLOR);
  draw_text(0, 16 * 3, "Down:  s", WHITE_COLOR);
  draw_text(0, 16 * 4, "Right: d", WHITE_COLOR);
  draw_text(0, 16 * 5, "Quit:  q", WHITE_COLOR);

  do {
    // Erase the old square
    draw_rect(x, y, 20, 20, 0);
    key = getkey();
    if (key == 'w')
      y -= 10;
    else if (key == 's')
      y += 10;
    else if (key == 'a')
      x -= 10;
    else if (key == 'd')
      x += 10;
    // Draw the new square
    draw_rect(x, y, 20, 20, 15);
    sleep_ms(20);
  } while(key != 'q');

  exit_graphics();
  return 0;
}
