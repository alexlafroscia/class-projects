class Heuristic(object):

    def get_cost(self, state):
        """
        Get the heuristic cost for some state

        Remember: smaller values will be picked with higher prescedence by
        the heap sort algorithm

        Returns:
            int: The cost for the given state
        """
        raise NotImplementedError("""Heuristics must be able to get the cost
                                     for a state!""")


class MaxMoves(Heuristic):

    def get_cost(self, state):
        p = state.num_pegs
        m = len(state.moves)
        return p - 1 - m / (m + 1)


class MinMoves(Heuristic):

    def get_cost(self, state):
        p = state.num_pegs
        m = len(state.moves)
        return p - 1 - 1 / (m + 1)


class MaxMovablePegs(Heuristic):

    def get_cost(self, state):
        p = state.num_pegs
        pegs_with_moves = map(lambda x: x.space_from, state.moves)
        unique_pegs_with_moves = []
        for space in pegs_with_moves:
            if space not in unique_pegs_with_moves:
                unique_pegs_with_moves.append(space)
        q = len(unique_pegs_with_moves)
        return p - 1 - q / p
