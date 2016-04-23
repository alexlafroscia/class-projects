# Flappy Bird (using Pygame)

We started with an interactive implementation of the game, removed the player controls, then built an AI "player" that learned how to play over time.  Mine actually got pretty good by the end.

## Choices Made

I chose to represent a state as the combination of the height of the pipe gap, the Y-height of the bird and the X-distance to the pipe.  In order to make my algorithm more efficient and limit the possible number of states, I made sure to use integers instead of floating-point decimals for these representations, since we don't want that kind of precision.  An additional change that I made was to evaluate the state on every 20 game ticks, which further limits the number of states and allows feedback about bad states (with a large negative reward) to propagate backward much more quickly.  The further I limited the possible number of states, the faster the bird learned.

## Training Time

Without varying the height of the pipes, the bird could be trained in around 40 games played, allowing it to get through over a hundred sets of pipes fairly quickly.  To make it more efficient, I would play with limiting the X-distance to the pipe in order to further limit the number of possible states.

## How to train the bird

N/A (I didn't have time to implement this part).  However, the game is sped up to play 5X the normal rate, so it does learn to play very quickly.

## Resources Used

- I discussed the project with some friends in a chat room for the class.  The only real help that I gained from here was advice on how to speed up the rate as which the bird plays the game.
