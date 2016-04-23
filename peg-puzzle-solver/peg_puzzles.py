import sys
from game import Board, Game
from player import Human, AI


def main(argv):
    game = Game(Board(argv[0]))
    if (len(argv) == 1):
        player = Human(game)
    else:
        # try:
        #     player = AI(game, argv[1:])
        # except:
        #     print("Invalid search parameters, please try again")
        #     exit()
        player = AI(game, argv[1:])

    player.play()


if __name__ == '__main__':
    main(sys.argv[1:])
