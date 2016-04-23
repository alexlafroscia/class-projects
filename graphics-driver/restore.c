void clear_screen();
void exit_graphics();
void init_graphics();

int main(int argc, char** argv)
{
  init_graphics();
  clear_screen();

  exit_graphics();
  return 0;
}
