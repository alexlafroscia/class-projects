import sys
from functools import reduce
from queue import Queue
from itertools import product,combinations


class Element(object):

    value = None
    name = None

    def __init__(self, param):
        if isinstance(param, tuple):
            (v, name) = param
            self.value = False
            self.name = name
        else:
            self.value = True
            self.name = param

    def is_inverse_of(self, other):
        return self.name == other.name and self.value != other.value

    def __bool__(self):
        return self.value

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    def __hash__(self):
        return hash(self.name) ^ hash(self.value)

    def __str__(self):
        return self.name + ", " + str(self.value)



class Sentence(object):

    elements = None

    def __init__(self, elements):
        """
        Create a new sentence with a list of elements

        Arguments:
            elements: Either an array of strings/tuples, or a set of Element
                      objects
        """
        self.elements = set()
        for el in elements:
            if not isinstance(el, Element):
                el = Element(el)
            self.elements.add(el)

    def resolve_with(self, other):
        """
        Resolve two sentences

        Arguments:
            other: The sentence to resolve with

        Returns:
            An array of parent sentence that were produced by the resolution
        """
        resolvants = set()
        combined_elements = product(self.elements, other.elements)
        for (x, y) in combined_elements:
            if x.is_inverse_of(y):
                new = self.elements.union(other.elements)
                new.remove(x)
                new.remove(y)
                resolvants.add(Sentence(new))
        return resolvants

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    def __hash__(self):
        if len(self.elements) > 1:
            return reduce(lambda x,y: hash(x) ^ hash(y), self.elements)
        if len(self.elements) == 1:
            return hash(next(iter(self.elements)))
        return 0

    def __str__(self):
        result = "Sentence: "
        for el in self.elements:
            result += "(" + str(el) + "), "
        return result[0:len(result) - 2]


def resolution(param):
    sentences = set()
    [sentences.add(Sentence(s)) for s in param]
    new = set()
    while 1:
        # Get the next two elements from the sentences
        for s1,s2 in combinations(sentences, 2):

            # Get the resolution
            resolution = s1.resolve_with(s2)

            # Check for an Empty Clause
            for p in resolution:
                if len(p.elements) == 0:
                    return False
            new = new.union(resolution)
        if new.issubset(sentences):
            return sentences
        sentences = sentences.union(new)


if __name__ == "__main__":
    model = eval(sys.argv[1])
    result = resolution(model)
    if result:
        for item in result.elements:
            print(item)
    else:
        print("There were no things")
