import unittest
from resolution import Sentence, resolution
from copy import deepcopy

kb = [[('not', 'Mythical'), ('not', 'Mortal')],
      ['Mythical', 'Mortal'],
      ['Mythical', 'Mammal'],
      ['Mortal', 'Horned'],
      [('not', 'Mammal'), 'Horned'],
      [('not', 'Horned'), 'Magical']]

class TestSentenceClass(unittest.TestCase):

    def test_small_sentences(self):
        s1 = Sentence([('not', 'P21'), 'B11'])
        s2 = Sentence([('not', 'B11')])
        resolvants = s1.resolve_with(s2)
        for p in resolvants:
            self.assertEqual(len(p.elements), 1)
            for item in p.elements:
                self.assertEqual(item.name, 'P21')

    def test_resolving_two_things(self):
        # (~a v ~b v c) ^ (a v b)
        s1 = Sentence([('not', 'a'), ('not', 'b'), 'c'])
        s2 = Sentence(['a', 'b'])
        resolution = s1.resolve_with(s2)
        self.assertEqual(len(resolution), 2)

class ClassExample(unittest.TestCase):

    def test_known_example(self):
        result = resolution([[('not', 'B11'), 'P12', 'P21'], [('not', 'P12'),
            'B11'], [('not', 'P21'), 'B11'], [('not', 'B11')], ['P12']])
        self.assertEqual(result, False)


class UnicornProblem(unittest.TestCase):

    def test_unicorn_horned(self):
        my_kb = deepcopy(kb)
        my_kb.append([('not', 'Horned')])
        result = resolution(my_kb)
        self.assertFalse(bool(result))

    def test_unicorn_magical(self):
        my_kb = deepcopy(kb)
        my_kb.append([('not', 'Magical')])
        result = resolution(my_kb)
        self.assertFalse(bool(result))

    def test_unicorn_mythical(self):
        my_kb = deepcopy(kb)
        my_kb.append([('not', 'Mythical')])
        result = resolution(my_kb)
        self.assertTrue(bool(result))


if __name__ == "__main__":
    unittest.main()
