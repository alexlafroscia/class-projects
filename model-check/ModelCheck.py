import sys
import itertools
from enum import Enum


class Validity(Enum):
    unsatisfiable = 0
    satisfiable = 1
    valid = 2


class Operator(object):

    operation = None

    def __init__(self, op):
        self.operation = op

    def evaluate(self, symbols):
        """
        Evaluate the passed-in symbols using the give operation

        Arguments:
            symbols:
                An array of symbols to operate one.  Can have one or more
                values.  Each symbol should have either a `true` or `false`
                value.

        Returns:
            Boolean -> Value based on result of operation
        """
        if self.operation == "not":
            return self._not(symbols[0])
        elif self.operation == "or":
            return self._or(symbols)
        elif self.operation == "and":
            return self._and(symbols)
        elif self.operation == "=>":
            return self._implies(symbols)
        elif self.operation == "<=>":
            return self._iff(symbols)
        return result

    def _not(self, symbol):
        """Boolean `not`"""
        return bool(not symbol)

    def _or(self, symbols):
        """Boolean `or`"""
        return bool(symbols[0] or symbols[1])

    def _and(self, symbols):
        """Boolean `and`"""
        return bool(symbols[0] and symbols[1])

    def _implies(self, symbols):
        """Boolean implication"""
        a = not symbols[0]
        return bool(a or symbols[1])

    def _iff(self, symbols):
        """Boolean equivalence"""
        a = symbols[0]
        b = symbols[1]
        return bool((a and b) or (not a and not b))


class Symbol(object):

    name = None

    parent = None
    """The sentence that this symbol belongs to"""

    symbol_list = []
    """
    Create a list of all of the symbols in use, so that we can track their
    truth value later
    """

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        if name not in Symbol.symbol_list:
            Symbol.symbol_list.append(name)

    def __bool__(self):
        table = self.parent.truth_row
        index = Symbol.symbol_list.index(self.name)
        return table[index]

    @classmethod
    def create_table(cls):
        """Return a table of truth values for each symbol"""
        n = len(cls.symbol_list)
        return list(itertools.product([False, True], repeat=n))


class Sentence(object):

    operator = None
    sentence = None

    _truth_row = None
    """Private holder for the truth row to evaluate against"""

    parent = None
    """
    The sentence that this sentence belongs to

    Will be None if the sentence is the outer-most one
    """

    def __init__(self, sentence, parent=None):
        self.operator = Operator(sentence[0])
        self.parent = parent
        self.sentence = list(map(lambda x: self._transform(x), sentence[1:]))

    def __bool__(self):
        """
        Get the boolean value of a Sentence

        Uses the underlying Operator object to evaluate the truth value of the
        Sentence.  Because a Sentence will be comprised of either Symbols or
        other Sentences, the Operator should be able to recursively evaluate
        inner Sentences automatically

        Returns:
            boolean -> The truth value of the sentence
        """
        return self.operator.evaluate(self.sentence)

    @property
    def truth_row(self):
        if self._truth_row is None and self.parent is not None:
            return self.parent.truth_row
        else:
            return self._truth_row

    @truth_row.setter
    def truth_row(self, value):
        if self.parent is not None:
            raise Error("You shouldn't be setting the row on a child sentence")
        self._truth_row = value

    def evaluate(self, truth_row):
        self.truth_row = truth_row
        return bool(self)

    def _transform(self, item):
        """Create either a Sentence or a Symbol given some type of input"""
        if type(item) is list:
            return Sentence(item, self)
        else:
            return Symbol(item, self)


def ModelCheck(model):
    s = Sentence(model)
    truth_values = Symbol.create_table()

    # Get the truth table value for every row in the table
    values = list(map(lambda row: s.evaluate(row), truth_values))
    return validity_check(values)


def validity_check(values):
    true_count = 0
    false_count = 0
    for val in values:
        if val:
            true_count += 1
        else:
            false_count += 1

    # Return our findings
    if true_count == len(values):
        return Validity.valid
    elif false_count == len(values):
        return Validity.unsatisfiable
    else:
        return Validity.satisfiable


# Initialize program if called from the command line
# Takes the first argument as a string and evaluates it to turn it into the array to process
if __name__ == "__main__":
    model = eval(sys.argv[1])
    result = ModelCheck(model)
    if result is Validity.unsatisfiable:
        print("Model is unsatisfiable")
    elif result is Validity.satisfiable:
        print("Model is satisfiable")
    elif result is Validity.valid:
        print("Model is valid")
