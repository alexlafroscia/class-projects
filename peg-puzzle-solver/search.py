from heapq import heappush, heappop
from queue import Queue, LifoQueue
from math import inf
from heuristics import MaxMoves, MinMoves, MaxMovablePegs


class SearchType(object):

    search_strategy = None
    """The search strategy to use for choosing states"""

    num_visited = 0
    """The number of states that were visited while searching"""

    max_space = 0
    """The largest size that the frontier list got while searching"""

    solution = None
    """The solution board, or None"""

    def __init__(self, start_state, search_strategy):
        self.search_strategy = search_strategy
        self.enqueue(start_state)

    def enqueue(self, state):
        self.search_strategy.push(state)
        frontier_size = self.search_strategy.size()
        if frontier_size > self.max_space:
            self.max_space = frontier_size

    @property
    def report(self):
        """Return a string that represets a "report" of the search results"""
        result = ""

        # Solution path
        result += "\nSolution path:"
        if self.solution is None:
            # Note: Whitespace set to align output with other results
            result += "         There was no solution path"
        else:
            result += "\n"
            temp_board = self.solution
            moves = []
            while temp_board.previous_board is not None:
                moves.append(temp_board.transition_move)
                temp_board = temp_board.previous_board
            moves.reverse()
            for move in moves:
                result += str(move) + "\n"

        # Num visited
        result += "\nNumber Visited (Time): {0}\n".format(self.num_visited)

        # Maximum Space Required
        result += "Space Required:        {0}".format(self.max_space)

        return result

    def run_search(self):
        board = None
        while board is None and not self.search_strategy.empty():
            board = self._run_search()
        self.solution = board
        return board

    def _run_search(self):
        """
        Run the search algorithm, starting with the state initialized with
        """
        board = self.search_strategy.pop()
        if board.num_pegs == 1:
            return board  # What do we actually want to return?
        else:
            moves = board.moves
            for index, move in enumerate(moves):
                next_board = board.execute_move(index)
                self.enqueue(next_board)
        return None


class TreeSearch(SearchType):
    """
    Tree Search Algorithm

    Does not account for duplicate items in the frontiers list
    """

    def __init__(self, start_state, search_strategy):
        SearchType.__init__(self, start_state, search_strategy)

    def enqueue(self, state):
        self.num_visited += 1
        super(TreeSearch, self).enqueue(state)


class GraphSearch(SearchType):
    """
    Graph Search Algorithm

    Does account for duplicate items in the frontiers list, and prevents them
    from being visited again
    """

    explored_list = []

    def __init__(self, start_state, search_strategy):
        SearchType.__init__(self, start_state, search_strategy)

    @property
    def report(self):
        result = super(GraphSearch, self).report
        result += "\n"
        result += "Explored List Items:   {0}".format(len(self.explored_list))
        return result

    def enqueue(self, state):
        """
        Adds an item to the frontiers list

        Relies on the parent class's implementation, but only adds the item
        if it hasn't been visited already
        """
        self.num_visited += 1
        if state not in self.explored_list:
            super(GraphSearch, self).enqueue(state)
            self.explored_list.append(state)


class IDAStar(SearchType):
    """
    Search method for IDAStar

    This search is a bit different than the others, in that it lends itself
    to being implemented outside the rhelm of Tree- or GraphSearch and
    therefore should really be a Search Type, not a Search Strategy.  This
    may have uncovered an inherent weakness in my implementation of the search
    pattern, but it's too late to change things too much now.  In the future,
    it might make more sense to implement a SearchStrategy that contains a
    SearchType, not the other way around
    """

    heuristic = None

    cut_off = None

    start_state = None

    def __init__(self, start_state, heuristic):
        if (heuristic == 'min_moves' or heuristic == 'min-moves'):
            self.heuristic = MinMoves()
        elif (heuristic == 'max_moves' or heuristic == 'max-moves'):
            self.heuristic = MaxMoves()
        elif (heuristic == 'max_movable_pegs' or
              heuristic == 'max-movable-pegs'):
            self.heuristic = MaxMovablePegs()
        else:
            raise Exception('Invalid heuristic type')

        # Initialize the cutoff value.  Implicit path cost of 0 at start
        self.cut_off = self.heuristic.get_cost(start_state)
        self.start_state = start_state

    def run_search(self):
        while True:
            # Either get the board or increase the cut-off of the next round
            board, self.cut_off = self._cost_limited_dfs()
            if board is not None:
                self.solution = board
                return board
            if self.cut_off == inf:
                self.solution = None
                return None

    def _cost_limited_dfs(self):
        """Run the DFS from a node

        Returns:
            (board, next_min)
            Board can either be a board or None
        """
        frontiers_list = Queue()
        frontiers_list.put(self.start_state)
        next_min = inf
        while True:
            if frontiers_list.empty():
                return (None, next_min)

            # Pop a node off the stack
            board = frontiers_list.get()
            cost = self._get_cost(board)

            # If the cost is less than the cutoff, we can continue
            if cost <= self.cut_off:
                if board.num_pegs == 1:
                    return (board, next_min)
                for index, move in enumerate(board.moves):
                    next_board = board.execute_move(index)
                    self.num_visited += 1
                    frontiers_list.put(next_board)
                    if self.max_space < frontiers_list.qsize():
                        self.max_space = frontiers_list.qsize()

            else:
                if cost < next_min:
                    next_min = cost

    def _get_cost(self, board):
        return self.heuristic.get_cost(board) + board.path_cost


class SearchStrategy(object):

    frontiers_list = None

    def push(self, state):
        raise NotImplementedError("Must be able to add a state")

    def pop(self):
        raise NotImplementedError("Must be able to remove a state")

    def size(self):
        raise NotImplementedError("""Must be able to get the size of the
                                     frontiers list""")

    def empty(self):
        raise NotImplementedError("Must be able to check if list is empty")


class BFS(SearchStrategy):

    def __init__(self):
        self.frontiers_list = Queue()

    def push(self, state):
        self.frontiers_list.put(state)

    def pop(self):
        return self.frontiers_list.get()

    def size(self):
        return self.frontiers_list.qsize()

    def empty(self):
        return self.frontiers_list.empty()


class DFS(BFS):

    def __init__(self):
        self.frontiers_list = LifoQueue()


class AStar(SearchStrategy):

    heuristic = None

    def __init__(self, heuristic):
        if (heuristic == 'min_moves' or heuristic == 'min-moves'):
            self.heuristic = MinMoves()
        elif (heuristic == 'max_moves' or heuristic == 'max-moves'):
            self.heuristic = MaxMoves()
        elif (heuristic == 'max_movable_pegs' or
              heuristic == 'max-movable-pegs'):
            self.heuristic = MaxMovablePegs()
        else:
            raise Exception('Invalid heuristic type')
        self.frontiers_list = []

    def push(self, state):
        cost = self.heuristic.get_cost(state) + state.path_cost
        heappush(self.frontiers_list, (cost, state))

    def pop(self):
        priority, state = heappop(self.frontiers_list)
        return state

    def size(self):
        return len(self.frontiers_list)

    def empty(self):
        return len(self.frontiers_list) == 0
