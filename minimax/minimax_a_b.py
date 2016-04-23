import sys
from math import inf


def successor_states(state):
    """Return the successor states for a given state"""
    if isinstance(state, list):
        return state[1:]
    else:
        return None


def max_value(state, alpha, beta):
    """
    Get the maximum value from the given state

    Returns:
        (max_value, num_visited)
    """

    num_visited = 1

    # Terminality test
    if isinstance(state, tuple):
        (name, value) = state
        return (value, num_visited)

    # Get value from successor states
    value = -inf
    for s in successor_states(state):
        (min_from_state, visited_at_state) = min_value(s, alpha, beta)
        num_visited += visited_at_state
        value = max(value, min_from_state)
        if value >= beta:
            return (value, num_visited)
        else:
            alpha = max(alpha, value)
    return (value, num_visited)


def min_value(state, alpha, beta):
    """
    Get the minimum value from the given state

    Returns:
        (min_value, num_visited)
    """

    num_visited = 1

    # Terminality test
    if isinstance(state, tuple):
        (name, value) = state
        return (value, num_visited)

    # Get value form siccessor states
    value = inf
    for s in successor_states(state):
        (max_from_state, visited_at_state) = max_value(s, alpha, beta)
        num_visited += visited_at_state
        value = min(value, max_from_state)
        if value <= alpha:
            return (value, num_visited)
        else:
            beta = min(beta, value)
    return (value, num_visited)


def minimax_a_b(state):
    return max_value(state, -inf, inf)

if __name__ == '__main__':
    # Note: This is probably *really* bad practice, but I'm assuming that no
    # one is trying to do anything too malicious with my homework assignment
    tree = eval(sys.argv[1])
    (value, visited) = minimax_a_b(tree)
    print('Utility value of root:   %s' % value)
    print('Number of notes visited: %s' % visited)
