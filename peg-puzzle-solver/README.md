# Assignment 1: Peg Solitaire

By: Alex LaFroscia
Python Version: 3.5.0

## Implementation Choices

I chose to implement each "piece" of the game (the Game, Board, Space, Move and Direction) as a separate class, in order to take advantage of Python's Object-Oriented nature.  This ended up helping a lot to keep the code clean and organized as opposed to, for example, just representing a space by the character that it would translate to on the board.  I learned a bit about Python classes' `__str__` and `__repr__` methods, which allowed me to keep the benefit of printing the Space class as a character but still have access to the helpful context of the class.

The state space is represented quite simply as a matrix of spaces, which is hidden as a private property within the Board class.  This allows for easy iteration over each space and creates boundaries regarding which spaces it can interact with that are easy to reason about.  I can't imagine implementing the board in any other way that would make as much sense, so I'm happy that I chose this method of implementation.

## Additional Resources

Since I'm not too familiar with the Python language, I consulted the documentation quite a bit, not just about how to use the language but also to learn about the style in which it is usually written.

In addition to the written resources, I also use the `Pyflakes` and `PEP8` static analytics tools to ensure that my code is standards compliant and error free.  I tried to use `mccabe` tool as well, but found it really hard to keep methods under 10 lines.  After a lot of refactoring, I was able to organize the code a lot better than my initial trial, but when there are 8 directions to consider, and each might have a single method to call, that's 16 lines already and broke the rule.

### Python API

- [Python API Docs](https://docs.python.org/3/)
- [Python Enumeration API](https://docs.python.org/3/library/enum.html)

### Python Coding Style

- [PEP 0257: Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [Hitchhiker's Guide to Python](http://docs.python-guide.org/en/latest/writing/documentation/)

## Persons Collaborated With

None

## Features Not Working

None

# Assignment 2: Peg Puzzles, AI Solutions

Python Version: 3.5

## Do the outcomes make sense?

For the most part, the outcomes of the assignment seem to make sense.  For each search performed, the Tree-Search runs less efficiently than Graph Search, since so many of the nodes get pruned out of being searched a second time.  DFS takes far less time to complete than BFS, which makes sense because it is technically not exhaustive and is able to get down into the leaf nodes much faster, giving it the possibility of finding a solution very quickly, while BFS is forced to iterate over every inner node before reaching a possible solution.  When done without pruning, BFS takes a _very_ long time to complete.  The one surprise ended up being IDAStar, which ended up taking a lot more space than I was expecting, more space than AStar.  I think that this might be due to an implementation error on my part, although I'm really not sure.  Since all of my test runs eventually found a solution, I would say that everything stood up to my expectations for completeness, since all of the example boards did have a solution and there were no algorithms that didn't find one.


## Was there anything that surprised you?

I was surprised by how quickly DFS is able to come up with a solution to the problem.  I figured that it would take longer than AStar, since the heuristics should help increase the search speed, but in reality DFS ends up finishing in mere seconds while AStar takes around two minutes to complete on my machine.  This, again, might be due to implementation details or just pure luck, since it's possible that DFS finds the solution path within the first few paths that it tries.  This possibility is alluded to by the fact that the number of nodes visited is very low.  I think that on a different problem, or if given a better heuristic, that AStar could be much more performant, but in these problems that are relatively small, uninformed search can perform faster.

## Best Heuristic for Informed Search

By far, minimizing the number of moves resulted in the fastest completion time and the least amount of space required to hold the data.  This seems intuitive, since minimizing the amount of moves gets us closer to the goal that we want to achieve, namely having zero moves left.  The other heuristics optimize for either maximizing the number of moves or the number of pegs, but neither of these makes sense as heuristics since they move us further away from what we know the goal state will look like.

## Different Puzzles

I did development against the SWNE board (where the board was a triangle instead of a square), so I ran the algorithms against that a number of times.  Generally, it performed comparably to the board we had to test against, in that if some configuration took less time than another with one board, the same would hold true for the other board.  Interestingly, the SWNE board actually took longer than the "all directions" board in the examples that I compared directly, which was surprising because there were less possible places that a peg could be moved to.
