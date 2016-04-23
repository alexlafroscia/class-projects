# Model Check

Python Version: 3.5.0

## Results from Book Problems

| Example | Result      |
| :-----: | :---------: |
| a       | Valid       |
| b       | Satisfiable |
| c       | Satisfiable |
| e       | Valid       |
| f       | Valid       |
| g       | Valid       |


## How to Run the Code

To run the code, pass the "model" as a string to the program as the first parameters, like so:

    $ python ModelCheck.py "['or', ['or', 'Smoke', 'Fire'], ['not', 'Fire']]"

The program will evaluate the string and parse out the value of the array.  I know that this is really dangerous normally, but in an environment like a homework assignment, I think that it's fine to assume no one is going to do anything too dangerous.

An easier way, however, might be to run the tests that I have already written and that are included as part of my submission.  You can do so by running

    $ python -m unittest test.TextbookProblems

Which will execute the tests defined in the `test.py` file as the `TextbookProblems` class.


## Not Working

N/A


## Other Comments

N/A
