from copy import deepcopy
from enum import Enum


class Game:

    board = None
    is_finished = False

    def __init__(self, board):
        self.board = board

    def select_move(self, selection):
        """
        Select a particular move to execute.

        Returns:
            bool: Whether or not the move was executed.  It would not be
            executed in cases where the selected move was too high to be a
            valid choice, or if the user input is not a choice at all.
        """
        # Reject the move if the input is not a number
        try:
            selection = int(selection)
        except ValueError:
            return False

        self.board = self.board.execute_move(selection)
        return True


class Board:

    movement_options = None
    width = None

    previous_board = None
    """The previous board configuration, before the current state"""

    transition_move = None
    """
    The move that transitioned the board from the previous state to the
    current one
    """

    path_cost = 0

    _matrix = None
    _latest_move_set = None

    def __init__(self, file_name):
        try:
            f = open(file_name)
            self.movement_options = f.readline().strip()
            self.width = int(f.readline())

            # Set up the _matrix based on the new width
            w = self.width
            self._matrix = [[None for x in range(w)] for x in range(w)]

            # Read in the _matrix and store it in memory
            for row in range(0, self.width):
                line = f.readline().strip().split(' ')
                for col in range(0, self.width):
                    self._matrix[row][col] = Space(line[col], row, col, self)
        finally:
            f.close()

    @property
    def moves(self):
        """Get all of the moves possible in the current board state."""
        all_moves = []
        for row in range(0, self.width):
            for col in range(0, self.width):
                moves = self._matrix[row][col].check_moves()
                if moves is not None and len(moves) > 0:
                    for move in moves:
                        all_moves.append(move)
        self._latest_move_set = all_moves
        return all_moves

    def find_valid_move(self, space_from, direction):
        """
        Find a move in the given direction from one space to another.

        Returns:
            (Space, Space): The first item returned is the ``to`` space, while
            second item is the ``between`` space.

            (None, None) will be returned if the move is invalid
        """
        # Check that the "to" location is valid
        space_to = self._get_loc_in_direction(space_from, direction, 2)
        if space_to is None or space_to.kind != 'Hole':
            return (None, None)

        space_between = self._get_loc_in_direction(space_from, direction, 1)
        if space_between is not None and space_between.kind == 'Peg':
            return (space_to, space_between)
        else:
            return (None, None)

    def _get_loc_in_direction(self, space_from, direction, distance):
        from_row = space_from.row
        from_col = space_from.col
        location = None

        if not space_from.can_move(direction):
            return location

        if direction is Direction.north:
            location = self._matrix[from_row - distance][from_col]
        elif direction is Direction.north_east:
            location = self._matrix[from_row - distance][from_col + distance]
        elif direction is Direction.east:
            location = self._matrix[from_row][from_col + distance]
        elif direction is Direction.south_east:
            location = self._matrix[from_row + distance][from_col + distance]
        elif direction is Direction.south:
            location = self._matrix[from_row + distance][from_col]
        elif direction is Direction.south_west:
            location = self._matrix[from_row + distance][from_col - distance]
        elif direction is Direction.west:
            location = self._matrix[from_row][from_col - distance]
        elif direction is Direction.north_west:
            location = self._matrix[from_row - distance][from_col - distance]

        return location

    def execute_move(self, index):

        # Reject the move if the number if too high to be a choice
        if index >= len(self._latest_move_set):
            return None

        # Make a new board object for the next state
        new_board = deepcopy(self)
        new_board.previous_board = self
        new_board.path_cost = self.path_cost + 1

        # Get the move for the transition
        move = new_board._latest_move_set[index]
        new_board.transition_move = move

        space_between = move.space_between

        # If the space between the two was a peg, "remove" it
        if space_between.kind == 'Peg':
            space_between.set_type('o')

        move.space_to.set_type('*')
        move.space_from.set_type('o')
        return new_board

    @property
    def num_pegs(self):
        """Get the number of pegs left on the board."""
        pegs = 0
        for row in range(0, self.width):
            for col in range(0, self.width):
                if self._matrix[row][col].kind == 'Peg':
                    pegs += 1
        return pegs

    def __str__(self):
        string = ''

        # Add the column numbers
        for x in range(0, self.width):
            string += ' ' + str(x)
        string += '\n'

        # Add the rows
        for row in range(0, self.width):
            part = str(row) + ' '
            part += ' '.join(str(v) for v in self._matrix[row]) + '\n'
            string += part
        return '  ' + string.strip()

    def __eq__(self, other):
        """
        Test the equality of two boards

        Equality is determined by comparing the "space" at each point in the
        matrix to see if they are of the same type
        """
        for row in range(0, self.width):
            for col in range(0, self.width):
                if not self._matrix[row][col] == other._matrix[row][col]:
                    return False
        return True

    def __lt__(self, other):
        return self.path_cost < other.path_cost


class Space:

    _character = None
    row = None
    col = None
    kind = None

    def __init__(self, _character, row, col, board):
        self.row = row
        self.col = col
        self.board = board
        self.set_type(_character)

    def set_type(self, _character):
        """Set the type of the space."""
        self._character = _character
        if self._character == '*':
            self.kind = 'Peg'
        elif self._character == 'o':
            self.kind = 'Hole'
        else:
            self.kind = 'Solid'

    def check_moves(self):
        """
        Get the moves that the current space can perform.

        Returns:
            Array: The array of moves that can be executed

            Will return ``None`` if the space is not a peg
        """
        moves = None
        if self.kind == 'Peg':
            moves = [move for move in self._check_ortho_moves()]
            if self.board.movement_options == 'swne':
                moves.extend(self._check_swne_moves())
            if self.board.movement_options == 'all':
                moves.extend(self._check_swne_moves())
                moves.extend(self._check_senw_moves())
        return moves

    def _check_ortho_moves(self):
        return self._check_moves_in_directions(Direction.north,
                                               Direction.east,
                                               Direction.south,
                                               Direction.west)

    def _check_swne_moves(self):
        return self._check_moves_in_directions(Direction.north_east,
                                               Direction.south_west)

    def _check_senw_moves(self):
        return self._check_moves_in_directions(Direction.south_east,
                                               Direction.north_west)

    def _check_moves_in_directions(self, *directions):
        moves = []
        for direction in directions:
            move = self._get_move(direction)
            if move is not None:
                moves.append(move)
        return moves

    def _get_move(self, direction):
        move = None
        (to, between) = self.board.find_valid_move(self, direction)
        if to is not None and between is not None:
            return Move(self, to, between)
        return move

    def can_move(self, direction):
        """
        Check if the peg can move in the given direction.

        Args:
            direction (Direction): The direction that should be checked in

        Returns:
            bool: True if the move can be performed, False if not
        """
        if direction is Direction.north:
            return self._can_move_north()
        elif direction is Direction.north_east:
            return self._can_move_north_east()
        elif direction is Direction.east:
            return self._can_move_east()
        elif direction is Direction.south_east:
            return self._can_move_south_east()
        elif direction is Direction.south:
            return self._can_move_south()
        elif direction is Direction.south_west:
            return self._can_move_south_west()
        elif direction is Direction.west:
            return self._can_move_west()
        elif direction is Direction.north_west:
            return self._can_move_north_west()

    def _can_move_north(self):
        return self.row > 1

    def _can_move_south(self):
        return self.row < self.board.width - 2

    def _can_move_east(self):
        return self.col < self.board.width - 2

    def _can_move_west(self):
        return self.col > 1

    def _can_move_north_east(self):
        return self._can_move_north() and self._can_move_east()

    def _can_move_south_west(self):
        return self._can_move_south() and self._can_move_west()

    def _can_move_north_west(self):
        return self._can_move_north() and self._can_move_west()

    def _can_move_south_east(self):
        return self._can_move_south() and self._can_move_east()

    def __str__(self):
        return self._character

    def __repr__(self):
        return '<Space Type:{0} Col:{1} Row:{2}>'.format(self.kind,
                                                         self.col,
                                                         self.row)

    def __hash__(self):
        return (self.kind, self.col, self.row)

    def __eq__(self, other):
        return self.kind == other.kind


class Move:
    """Represent a move that can be performed by a peg."""

    space_from = None
    space_to = None
    space_between = None
    """
    The space between the "to" and "from" peg, that will be removed after
    the move is complete
    """

    def __init__(self, space_from, space_to, space_between):
        self.space_from = space_from
        self.space_to = space_to
        self.space_between = space_between

    def __str__(self):
        return '( {0}, {1} ) --> ( {2}, {3} )'.format(self.space_from.col,
                                                      self.space_from.row,
                                                      self.space_to.col,
                                                      self.space_to.row)


class Direction(Enum):
    """Represent the directions that a peg can move in."""

    north = 1
    north_east = 2
    east = 3
    south_east = 4
    south = 5
    south_west = 6
    west = 7
    north_west = 8
