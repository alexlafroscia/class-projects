# Boggle

##Goal:
To demonstrate knowledge of both exhaustive search of a problem space and lookup search through the implementation of a modified version of the game Boggle.

##Background:
Given a 4x4 grid of letters, Boggle is played by having users identify as many valid English words of at least three characters that can be made by joining adjacent letters on the boggle board.
Adjacent letters can be found horizontally, vertically, or diagonally next to one another.
Note that the same space the grid cannot be used twice in a given word.

Consider the following board:

| | | | |
|---|---|---|---|
|F|R|O|O|
|Y|I|E|S|
|L|D|N|T|
|A|E|R|E|

FRIEND, ROSTER, and FROST are all valid words.
DEAD is not a valid word as you would need to use the same D twice to construct it.

For this assignment, we will consider a modified version of Boggle where wildcard characters are allowed.
The "*" character will be considered a wildcard and can be considered any letter of the alphabet when constructing words.
For example, in the following board:

| | | | |
|---|---|---|---|
|F|R|O|O|
|Y|I|E|S|
|L|*|N|T|
|A|E|R|E|

RIVER, RING, and TRAIL are all valid words where they would not have been in the previous puzzle.

## Additional Comments:

- DLB dictonary class can handle the wildcard board spaces just fine
- Simple dictionary class is too slow to handle the wildcard board spaces
- I added parallelism to handle the fact that the board can be searched at the same time
  as the user is inputting the guesses.  So, when running the simple dictionary with a
  wildcard board, it might delay response after the user finishes entering guesses, which
  might not be what you're expecting.  However, I decided that it was a solid trade off
  to improve the user's experience when running any other board, since there is no wait
  time experienced by the user.
