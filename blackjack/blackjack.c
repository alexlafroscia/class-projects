/*
 * Blackjack.c
 * Alex LaFroscia
 * Sep 12, 2014
 *
 *
 */

#include<stdio.h>

int main()
{
  int dealer_sum;
  int dealer_first;
  int dealer_has_ace = 0;

  int player_sum;
  int player_first;
  int player_second;
  int player_add_value;
  int player_has_ace = 0;
  int player_wants_hit = 1;

  char hit_response[256];

  // Seed for random numbers
  srand((unsigned int)time(NULL));

  // Determine the dealer's hand
  dealer_first = pick_card();
  dealer_sum = dealer_first;
  if (dealer_first == 11) {
    dealer_has_ace = 1;
  }
  do {
    dealer_sum = dealer_sum + pick_card();
    if (dealer_sum > 21 && dealer_has_ace == 1) {
      dealer_sum = dealer_sum - 10;
      dealer_has_ace = 0;
    }
  } while (dealer_sum < 17);

  printf("The dealer:\n");
  printf("? + %d\n", dealer_first);

  printf("\nYou:\n");
  player_first = pick_card();
  if (player_first == 11) {
    player_has_ace = 1;
  }
  player_second = pick_card();
  if (player_second == 11) {
    if (player_has_ace == 1) {
      player_second = 1;
    } else {
      player_has_ace = 1;
    }
  }
  player_sum = player_first + player_second;
  printf("%d + %d = %d\n", player_first, player_second, player_sum);

  while (player_sum < 21 && player_wants_hit == 1)
  {
    printf("\nWould you like to “hit” or “stand”? ");
    scanf("%s", hit_response);

    if (strcmp(hit_response,"hit") == 0)
    {
      player_add_value = pick_card();
      if (player_sum + player_add_value > 21 && player_has_ace == 1) {
        player_sum = player_sum - 10;
        player_has_ace = 0;
      }

      if (player_add_value == 11) {
        player_has_ace = 1;
      }

      if (player_sum + player_add_value > 21) {
        player_add_value = 1;
        player_has_ace = 0;
      }

      printf("\nYou:\n%d + %d = %d\n", player_sum, player_add_value, player_sum + player_add_value);
      player_sum += player_add_value;
    }
    else if (strcmp(hit_response,"stand") == 0)
    {
      player_wants_hit = 0;
    }
  }


  if (dealer_sum == 21) {
    printf("\nThe dealer got 21.\n\nYou lose.\n");
  } else if (player_sum == 21) {
    printf("\nYou got 21.\n\nYou win.\n");
  } else if (player_sum == dealer_sum) {
    printf("\nYou and the dealer both had %d.\n", dealer_sum);
    printf("But the dealer wins.\n\nSorry.\n");
  } else if (player_sum > 21) {
    printf("\nYou had %d and busted.\n\nYou lose.\n", player_sum);
  } else if (dealer_sum > 21) {
    printf("\nThe dealer had %d and busted.\n\nYou win.\n", dealer_sum);
  } else if (dealer_sum > player_sum) {
    printf("\nThe dealer was closer to 21 with a total of %d.\n", dealer_sum);
    printf("You had a total of %d.\n", player_sum);
    printf("\nYou lose.\n");
  } else {
    printf("\nYou were closer to 21 with a total of %d.\n", player_sum);
    printf("The dealer had a total of %d.\n", dealer_sum);
    printf("\nYou win.\n");
  }

  printf("\n");
  return 0;
}

int pick_card()
{
  int value = rand() % 12;
  int return_value;

  switch(value)
  {
    case 0:
      return_value = 10;
      break;
    case 1:
      return_value = 11;
      break;
    case 11:
      return_value = 10;
      break;
    case 12:
      return_value = 10;
      break;
    default:
      return_value = value;
      break;
  }

  return return_value;
}
