from enum import Enum
from contextlib import contextmanager
from random import randint


OVERALL_SPEED = 5
ANIMATION_SPEED = 0.18 * OVERALL_SPEED  # pixels per millisecond
FPS = 60
WIN_HEIGHT = 512
WIN_WIDTH = 284 * 2     # BG image size: 284x512 px; tiled twice

EXPLORATION_CONSTANT = 300


def get_pipe_middle(pipe):
    """
    Find the height of the middle of the gap in a pair of pipes
    """
    gap_height = WIN_HEIGHT - pipe.bottom_height_px - pipe.top_height_px
    return pipe.top_height_px + (gap_height / 2)


def get_first(array, default=None):
    if array:
        for item in array:
            return item
    return default


class Action(Enum):
    quit = 1
    flap = 2
    no_flap = 3


class StateWithAction(object):

    utility_values = dict()

    def __init__(self):
        self.utility_value = 0
        self.count = 0

    @classmethod
    def get_or_create(cls, state, action, count_state=True):
        """
        Get or create a StateWithAction object for some state and action

        Needs to perform a "get or create"-type action because we want to only
        ever have one copy of the State/Action pair, which we always update.
        We also want to keep track of how many times we've been in this state,
        so we need to be able to have a single, incremented count to do so.
        """
        state_with_action = cls.find(state, action)
        if count_state:
            state_with_action.count += 1
        if state_with_action.count == 1:
            print('New state')
        elif state_with_action.count != 0:
            print('Existing state')
        return state_with_action

    @classmethod
    def find(cls, state, action):
        """
        Find a StateWithAction object for some state and action

        May need to create the StateWithAction for the pair if it does not
        already exist.  This is not a problem, because if we don't increment
        the count or update the utility value, then it's still as if we never
        visited the state before.
        """
        lookup_value = (state, action)
        if lookup_value not in cls.utility_values:
            cls.utility_values[lookup_value] = StateWithAction()
        return cls.utility_values[lookup_value]

    def update_utility_value(self, next_state, reward):
        alpha = 1 / self.count
        gamma = .9

        q_sample = reward + (gamma * next_state.max_value)
        old_value = self.utility_value
        self.utility_value = (1 - alpha) * old_value + alpha * q_sample

    def __hash__(self):
        return (hash(self.state) << 1) ^ hash(self.action)

    def __eq__(self, other):
        return hash(self) == hash(other)


class GameState(object):
    """
    The state of the game during one "tick"

    Attibutes:
        bird_state_x (int): the bird's x-coordinate
        bird_state_y (int): the bird's y-coordinate
    """
    last_state = None

    def __init__(self, bird, pipes):
        closest_pipe = get_first(pipes)
        self.bird_state_y = int(bird.y / 10)
        if closest_pipe is not None:
            self.pipe_middle = get_pipe_middle(closest_pipe)
            self.pipe_distance = int(closest_pipe.x - bird.x)
        else:
            self.pipe_middle = None
            self.pipe_distance = None

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return (hash(self.bird_state_y) << 2) ^ (
            hash(self.pipe_middle) << 1) ^ (
            hash(self.pipe_distance))

    @property
    def max_value(self):
        """
        Get the maximum value possible from this state

        Evaluates the utility values for each possible state/action combination
        and returns the best value.
        """
        return self._max_value_object[0]

    @property
    def max_value_action(self):
        """
        Get the action that results in the maximum value possible from this
        state

        Evaluates the utility values for each possible state/action combination
        and returns the action that results in the best one.
        """
        return self._max_value_object[1]

    @property
    def _max_value_object(self):
        flap = StateWithAction.find(self, Action.flap)
        flap_v = flap.utility_value + EXPLORATION_CONSTANT / (flap.count + 1)

        no_flap = StateWithAction.find(self, Action.no_flap)
        no_flap_v = (no_flap.utility_value +
                     EXPLORATION_CONSTANT / (no_flap.count + 1))

        if flap_v == no_flap_v:
            if (randint(0, 1) == 0):
                return (flap.utility_value, Action.flap)
            else:
                return (no_flap.utility_value, Action.no_flap)
        elif flap_v > no_flap_v:
            return (flap.utility_value, Action.flap)
        else:
            return (no_flap.utility_value, Action.no_flap)

    @contextmanager
    def take_action(self, action, count_state=True):
        """
        Yield a state/action combination for this state

        Something sort of weird was chosen for the implementation, to practice
        using Generators in Python; instead of passing the next state _into_
        the function, the state/action combination is passed _out_ of the
        function so that we can have the new state access it and update the
        utility value of this state
        """
        state_with_action = StateWithAction.get_or_create(self,
                                                          action,
                                                          count_state)
        yield state_with_action

    @classmethod
    def get_state(cls, bird, pipe):
        state = GameState(bird, pipe)
        cls.last_state = state
        return state

    @classmethod
    def should_jump(cls):
        return False
