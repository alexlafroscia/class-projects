from search import TreeSearch, GraphSearch, BFS, DFS, AStar, IDAStar


class Player(object):

    def play(self):
        raise NotImplementedError("Players need to play!")


class Human(Player):

    game = None

    def __init__(self, game):
        self.game = game

    def play(self):
        """
        Start an interactive session to play the game

        Returns:
            Whether or not the game was won
        """
        did_win = None
        while (not self.game.is_finished):
            did_win = self._execute_loop()

        # Print message to user
        if did_win:
            print('Congrats, you solved the puzzle!')
        else:
            print('Sorry, you ran out of moves. Please try again.')

        return did_win

    def _execute_loop(self):
        """Execute one iteration of the game loop."""
        game = self.game
        print('\n' + str(game.board) + '\n')
        moves = game.board.moves

        # Check end game conditions
        if len(moves) == 0:
            game.is_finished = True
            if game.board.num_pegs == 1:
                return True
            else:
                return False

        # Propose moves
        for move in range(0, len(moves)):
            string = str(move) + ' :   '
            string += str(moves[move])
            print(string)
        user_input = input('\nPlease select a move (or \'q\' to quit): ')
        if user_input == 'q':
            exit()
        if not game.select_move(user_input):
            print('\nPlease select a valid input')


class AI(Player):

    game = None
    """The game to play"""

    search_strategy = None
    """
    An object of type SearchType, that will control how the seach is performed
    """

    def __init__(self, game, ai_information):
        self.game = game

        # Capture AI settings that the user specified
        search_type = ai_information[0]
        search_strategy = ai_information[1]

        # Set the strategy to use to search with
        if search_strategy == "bfs":
            search_strategy = BFS()
        elif search_strategy == "dfs":
            search_strategy = DFS()
        elif search_strategy == "astar":
            search_strategy = AStar(ai_information[2])
        elif search_strategy == "idastar":
            self.search_strategy = IDAStar(game.board, ai_information[2])
        else:
            raise Exception('Invalid search stategy')

        if search_strategy == "idastar":
            pass
        elif (search_type == "tree-search"):
            self.search_strategy = TreeSearch(game.board, search_strategy)
        elif (search_type == "graph-search"):
            self.search_strategy = GraphSearch(game.board, search_strategy)
        else:
            raise Exception('Invalid search type')

    def play(self):
        """
        Start an AI session to play the game

        Returns:
            Whether or not the game was won
        """
        self.search_strategy.run_search()
        print(self.search_strategy.report)
        return True
