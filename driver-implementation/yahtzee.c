/*
 * Yahtzee!
 * Author: Alex LaFroscia
 * Date: Nov 13, 2014
 */

#include <stdio.h>
#include <string.h>
#include <time.h>

// Struct Definitions
typedef struct score {
  unsigned int ones;
  unsigned int twos;
  unsigned int threes;
  unsigned int fours;
  unsigned int fives;
  unsigned int sixes;
  unsigned int upper_bonus;
  unsigned int three_of_kind;
  unsigned int four_of_kind;
  unsigned int full_house;
  unsigned int small_straight;
  unsigned int large_straight;
  unsigned int yahtzee;
  unsigned int chance;
  unsigned int total;
} Score;


// Function Prototypes
unsigned int roll_die();
void print_score(Score*);
int give_placement_options(Score*);
void add_upper_section_score(unsigned int*, Score*, unsigned int);
void add_straight_score(unsigned int*, Score*, unsigned int);
void add_of_a_kind_score(unsigned int*, Score*, unsigned int);
void add_chance_score(unsigned int*, Score*);
void add_full_house_score(unsigned int*, Score*);
int cmpfunc (const void *, const void *);
void set_total_score(Score*);


/*
 * Main
 */
int main() {
  srand(time(NULL));

  int round = 1;
  // Score keeps track of the actual score of the player
  Score score_struct = {};
  Score *score = &score_struct;
  // Used Categories keeps track of which categories have been used by
  // the player.  I can't use 0s in the score struct, since the score
  // struct can hold a 0 for a used category as well, and I can't
  // substitute a null.  Stupid static typing!
  Score used_categories_struct = {};
  Score *used_categories = &used_categories_struct;

  while (round < 14) {
    int rerolls = 0;
    unsigned int dice[] = {
      roll_die(),
      roll_die(),
      roll_die(),
      roll_die(),
      roll_die(),
      roll_die()
    };

    do {

      if (rerolls == 0)
        printf("Your roll:\n\n");
      if (rerolls == 1)
        printf("\nYour second roll:\n\n");
      if (rerolls == 2)
        printf("\nYour third roll:\n\n");

      // Print out the dice roll
      printf("%d, %d, %d, %d, %d\n\n",
          dice[0], dice[1], dice[2], dice[3], dice[4], dice[5]);

      // Use the loop to print the dice rolls again, then break
      // the loop to move on
      if (rerolls == 2)
        break;

      char input[11];

      // Generate some random numbers
      // Print them out
      printf("Which dice to reroll? ");

      // Get the array of numbers
      fgets(input, 11, stdin);

      int length = strlen(input);

      if (input[0] == '0') {
        break;
      } else {
        int i;
        for(i = 0; i < length; i++) {
          switch (input[i])
          {
            case '1':
              dice[0] = roll_die();
              break;
            case '2':
              dice[1] = roll_die();
              break;
            case '3':
              dice[2] = roll_die();
              break;
            case '4':
              dice[3] = roll_die();
              break;
            case '5':
              dice[4] = roll_die();
              break;
            case '6':
              dice[5] = roll_die();
              break;
            case ' ':
            case '\n':
              break;
            default:
              printf("Invalid input!\n");
              break;
          }
        }
        rerolls++;
      }

    } while (rerolls < 3);

    // Sort the dice
    qsort(dice, 5, sizeof(unsigned int), cmpfunc);

    // Prompt for which section to place dice into
    int selection = give_placement_options(used_categories);
    switch (selection)
    {
      case 1:
      case 2:
      case 3:
      case 4:
      case 5:
      case 6:
        add_upper_section_score(dice, score, selection);
        break;
      case 7:
        add_of_a_kind_score(dice, score, 3);
        break;
      case 8:
        add_of_a_kind_score(dice, score, 4);
        break;
      case 9:
        add_full_house_score(dice, score);
        break;
      case 10:
        add_straight_score(dice, score, 4);
        break;
      case 11:
        add_straight_score(dice, score, 5);
        break;
      case 12:
        add_of_a_kind_score(dice, score, 5);
        break;
      case 13:
        add_chance_score(dice, score);
        break;
    }

    set_total_score(score);

    // Handle adding score

    printf("\nYour score so far is: %d\n\n", score->total);
    print_score(score);
    round++;

  } // End of round loop!

  printf("End of game!\n");
}

/*
 * Roll Die
 *
 * Returns a random number between 1 and 6
 */
unsigned int roll_die() {
  unsigned int r;
  unsigned char c;
  int read;
  FILE *fp;

  fp = fopen("/dev/dice", "r");

  do {
    read = fread(&c, sizeof(unsigned char), 1, fp);
  } while (!read);

  r = c;
  return r;
}


/*
 * Print Score
 *
 * Given a score struct pointer, print out the the current
 * score
 *
 * Arguments:
 *    Score*
 */
void print_score(Score *score) {
  printf("%-20s %3d ",  "Ones:",                 score->ones);
  printf("%-20s %3d\n", "Fours:",                score->fours);
  printf("%-20s %3d ",  "Twos:",                 score->twos);
  printf("%-20s %3d\n", "Fives:",                score->fives);
  printf("%-20s %3d ",  "Threes:",               score->threes);
  printf("%-20s %3d\n", "Sixes:",                score->sixes);
  printf("%-20s %3d\n", "Upper Section Bonus:",  score->upper_bonus);
  printf("%-20s %3d ",  "Three of a Kind:",      score->three_of_kind);
  printf("%-20s %3d\n", "Four of a Kind:",       score->four_of_kind);
  printf("%-20s %3d ",  "Small Straight:",       score->small_straight);
  printf("%-20s %3d\n", "Large Straight:",       score->large_straight);
  printf("%-20s %3d ",  "Full House:",           score->full_house);
  printf("%-20s %3d\n", "Yahtzee:",              score->yahtzee);
  printf("%-20s %3d\n", "Chance:",               score->chance);
  printf("\n");
}


/*
 * Gice palcement options
 *
 * Runs the menu that allows the user to choose which
 * category to place the dice in.  Does not show
 * used categories
 *
 * Arguments:
 *   Score*     The struct representing which categories have been used
 *
 * Returns:
 *   int        An int representing the user's choice
 */
int give_placement_options(Score *used) {
  int valid_choice;
  int selection = 0;
  char placement[0];

  do {
    valid_choice = 1;
    printf("\nPlace dice into:\n");

    if (!used->ones || !used->twos || !used->threes || !used->fours
        || !used->fives || !used->sixes) {
      printf("1) Upper Section\n");
    }

    if (!used->three_of_kind || !used->four_of_kind || !used->full_house
        || !used->small_straight || !used->large_straight || !used->yahtzee
        || !used->chance) {
      printf("2) Lower Section\n");
    }

    printf("\nSelection? ");

    // Read three characters -- The one to pick, the newline, and the null
    // terminator, so that we don't leave anthing in the buffer
    fgets(placement, 3, stdin);

    printf("\nPlace dice into:\n");

    if (placement[0] == '1') {
      if (!used->ones)
        printf("1) Ones\n");
      if (!used->twos)
        printf("2) Twos\n");
      if (!used->threes)
        printf("3) Threes\n");
      if (!used->fours)
        printf("4) Fours\n");
      if (!used->fives)
        printf("5) Fives\n");
      if (!used->sixes)
        printf("6) Sixes\n");

      printf("\n");

      fgets(placement, 3, stdin);

      switch (placement[0])
      {
        case '1':
          if (used->ones) {
            printf("Invalid option, try again!\n");
            valid_choice = 0;
          } else {
            selection = 1;
            used->ones = 1;
          }
          break;
        case '2':
          if (used->twos) {
            printf("Invalid option, try again!\n");
            valid_choice = 0;
          } else {
            selection = 2;
            used->twos = 1;
          }
          break;
        case '3':
          if (used->threes) {
            printf("Invalid option, try again!\n");
            valid_choice = 0;
          } else {
            selection = 3;
            used->threes = 1;
          }
          break;
        case '4':
          if (used->fours) {
            printf("Invalid option, try again!\n");
            valid_choice = 0;
          } else {
            selection = 4;
            used->fours = 1;
          }
          break;
        case '5':
          if (used->fives) {
            printf("Invalid option, try again!\n");
            valid_choice = 0;
          } else {
            selection = 5;
            used->fives = 1;
          }
          break;
        case '6':
          if (used->sixes) {
            printf("Invalid option, try again!\n");
            valid_choice = 0;
          } else {
            selection = 6;
            used->sixes = 1;
          }
          break;
        default:
          printf("Invalid option, try again!\n");
          valid_choice = 0;
          break;
      } // End switch statement

    } else if (placement[0] == '2') {
      if (!used->three_of_kind)
        printf("1) Three of a kind\n");
      if (!used->four_of_kind)
        printf("2) Four of a kind\n");
      if (!used->full_house)
        printf("3) Full House\n");
      if (!used->small_straight)
        printf("4) Small straight\n");
      if (!used->large_straight)
        printf("5) Large straight\n");
      if (!used->yahtzee)
        printf("6) Yahtzee\n");
      if (!used->chance)
        printf("7) Chance\n");

      printf("\n");

      fgets(placement, 3, stdin);

      switch (placement[0])
      {
        case '1':
          if (used->three_of_kind) {
            printf("Invalid option, try again!\n");
            valid_choice = 0;
          } else {
            selection = 7;
            used->three_of_kind = 1;
          }
          break;
        case '2':
          if (used->four_of_kind) {
            printf("Invalid option, try again!\n");
            valid_choice = 0;
          } else {
            selection = 8;
            used->four_of_kind = 1;
          }
          break;
        case '3':
          if (used->full_house) {
            printf("Invalid option, try again!\n");
            valid_choice = 0;
          } else {
            selection = 9;
            used->full_house = 1;
          }
          break;
        case '4':
          if (used->small_straight) {
            printf("Invalid option, try again!\n");
            valid_choice = 0;
          } else {
            selection = 10;
            used->small_straight = 1;
          }
          break;
        case '5':
          if (used->large_straight) {
            printf("Invalid option, try again!\n");
            valid_choice = 0;
          } else {
            selection = 11;
            used->large_straight = 1;
          }
          break;
        case '6':
          if (used->yahtzee) {
            printf("Invalid option, try again!\n");
            valid_choice = 0;
          } else {
            selection = 12;
            used->yahtzee = 1;
          }
          break;
        case '7':
          if (used->chance) {
            printf("Invalid option, try again!\n");
            valid_choice = 0;
          } else {
            selection = 13;
            used->chance = 1;
          }
          break;
        default:
          printf("Invalid option, try again!\n");
          valid_choice = 0;
          break;
      } // End switch statement
    } else {
      printf("\nInvalid input: try again!\n");
      valid_choice = 0;
    }

  } while (valid_choice == 0);

  return selection;
}

/*
 * Add upper section score
 *
 * Gets the score for one of the upper section categories,
 * given the category to calculate
 *
 * Arguments
 *   unsigned int *dice     The current dice
 *   Score *score           The current score
 *   unsigned int num       The category to calculate
 *
 */
void add_upper_section_score(unsigned int *dice, Score *score, unsigned int num)
{
  unsigned int result = 0;
  int i;
  for (i = 0; i < 5; i++) {
    if (dice[i] == num) {
      result += num;
    }
  }

  switch (num)
  {
    case 1:
      score->ones = result;
      break;
    case 2:
      score->twos = result;
      break;
    case 3:
      score->threes = result;
      break;
    case 4:
      score->fours = result;
      break;
    case 5:
      score->fives = result;
      break;
    case 6:
      score->sixes = result;
      break;
    default:
      break;
  }

  int upper_total = score->ones + score->twos + score->threes
    + score->fours + score->fives + score->sixes;
  if (upper_total > 63) {
    score->upper_bonus = 35;
  }
}


/*
 * Add Straight Score
 *
 * Paramters:
 *   unsigned int *dice
 *   Score *score
 *   unsigned int num
 *
 * `num` should either be 4 or 5 based on whether it should be a small
 * or large straight
 */
void add_straight_score(unsigned int *dice, Score *score, unsigned int num)
{
  unsigned int ones  = 0, twos  = 0, threes = 0, fours = 0;
  unsigned int fives = 0, sixes = 0, total  = 0;

  int i;
  for(i = 0; i < 5; i++) {
    total += dice[i];
    switch (dice[i])
    {
      case 1:
        ones++;
        break;
      case 2:
        twos++;
        break;
      case 3:
        threes++;
        break;
      case 4:
        fours++;
        break;
      case 5:
        fives++;
        break;
      case 6:
        sixes++;
        break;
    }
  } // End for loop

  if (num == 4) {
    if ((ones   >= 1 && twos   >= 1 && threes >= 1 && fours >= 1) ||
        (twos   >= 1 && threes >= 1 && fours  >= 1 && fives >= 1) ||
        (threes >= 1 && fours  >= 1 && fives  >= 1 && sixes >= 1) )
    {
      score->small_straight = 30;
    }
    return;
  }

  if (num == 5) {
    if ((ones == 1 || sixes == 1) && twos == 1 && threes == 1 &&
        fours == 1 && fives == 1 )
    {
      score->large_straight = 40;
    }
    // Return to exit function
    return;
  }

}


/*
 * Add Full House Score
 */
void add_full_house_score(unsigned int *dice, Score *score)
{
  unsigned int ones  = 0, twos  = 0, threes = 0, fours = 0;
  unsigned int fives = 0, sixes = 0, total  = 0;
  int two_group = 0;
  int three_group = 0;

  int i;
  for(i = 0; i < 5; i++) {
    total += dice[i];
    switch (dice[i])
    {
      case 1:
        ones++;
        break;
      case 2:
        twos++;
        break;
      case 3:
        threes++;
        break;
      case 4:
        fours++;
        break;
      case 5:
        fives++;
        break;
      case 6:
        sixes++;
        break;
    }
  } // End for loop

  if (ones == 3 || twos == 3 || threes == 3 || fours == 3 ||
      fives == 3 || sixes == 3)
  {
    two_group = 1;
  }

  if (ones == 2 || twos == 2 || threes == 2 || fours == 2 ||
      fives == 2 || sixes == 2)
  {
    three_group = 1;
  }

  if (two_group && three_group) {
    score->full_house = 25;
  }
}


/*
 * Sort function for the below function
 */
int cmpfunc(const void * a, const void * b)
{
  return ( *(int*)a - *(int*)b );
}


/*
 * Sort Dice
 *
 * Take a dice pointer, sort it, that's it
 */
void sort_dice(unsigned int *dice)
{
  qsort(dice, 5, sizeof(unsigned int), cmpfunc);
}


/*
 * Add of a Kind Score
 *
 * Paramters:
 *   unsigned int *dice
 *   Score *score
 *   unsigned int num
 *
 * `num` should either be 3, 4 or 5 based on whether it should be a
 * small or large straight
 */
void add_of_a_kind_score(unsigned int *dice, Score *score, unsigned int num)
{
  unsigned int ones  = 0, twos  = 0, threes = 0, fours = 0;
  unsigned int fives = 0, sixes = 0, total  = 0;

  int i;
  for(i = 0; i < 5; i++) {
    total += dice[i];
    switch (dice[i])
    {
      case 1:
        ones++;
        break;
      case 2:
        twos++;
        break;
      case 3:
        threes++;
        break;
      case 4:
        fours++;
        break;
      case 5:
        fives++;
        break;
      case 6:
        sixes++;
        break;
    }
  } // End for loop

  if (ones == num || twos == num || threes == num || fours == num ||
      fives == num || sixes == num)
  {
    switch (num)
    {
      case 3:
        score->three_of_kind = total;
        break;
      case 4:
        score->four_of_kind = total;
        break;
      case 5:
        score->yahtzee = 50;
        break;
    }
  }
}


/*
 * Add chance score
 */
void add_chance_score(unsigned int *dice, Score *score)
{
  int total = 0, i;
  for (i = 0; i < 5; i++) {
    total += dice[i];
  }
  score->chance = total;
}


/*
 * Set total score
 *
 * Calculates the total score based on all of the
 * category scores
 */
void set_total_score(Score *score)
{
  int total = 0;
  total += score->ones;
  total += score->twos;
  total += score->threes;
  total += score->fours;
  total += score->fives;
  total += score->sixes;
  total += score->upper_bonus;
  total += score->three_of_kind;
  total += score->four_of_kind;
  total += score->full_house;
  total += score->small_straight;
  total += score->large_straight;
  total += score->yahtzee;
  total += score->chance;

  score->total = total;
}
