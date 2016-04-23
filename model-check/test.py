import unittest
from ModelCheck import Sentence, Symbol, Operator, ModelCheck, Validity


class TestOperatorClass(unittest.TestCase):

    def test_not(self):
        o = Operator('not')
        self.assertTrue(o.evaluate([False]))
        self.assertFalse(o.evaluate([True]))

    def test_or(self):
        o = Operator('or')
        self.assertTrue(o.evaluate([True, True]))
        self.assertTrue(o.evaluate([True, False]))
        self.assertTrue(o.evaluate([False, True]))
        self.assertFalse(o.evaluate([False, False]))

    def test_and(self):
        o = Operator('and')
        self.assertTrue(o.evaluate([True, True]))
        self.assertFalse(o.evaluate([True, False]))
        self.assertFalse(o.evaluate([False, True]))
        self.assertFalse(o.evaluate([False, False]))

    def test_implies(self):
        o = Operator("=>")
        self.assertTrue(o.evaluate([True, True]))
        self.assertTrue(o.evaluate([False, True]))
        self.assertTrue(o.evaluate([False, False]))
        self.assertFalse(o.evaluate([True, False]))

    def test_iff(self):
        o = Operator("<=>")
        self.assertTrue(o.evaluate([True, True]))
        self.assertTrue(o.evaluate([False, False]))
        self.assertFalse(o.evaluate([True, False]))
        self.assertFalse(o.evaluate([False, True]))


class TestSentenceClass(unittest.TestCase):

    def test_init_with_symbols(self):
        s = Sentence(['or', 'Fire', 'Ice'])
        s.truth_row = 'test'
        self.assertEqual(type(s.sentence[0]), Symbol)
        self.assertEqual(type(s.sentence[1]), Symbol)
        self.assertEqual(s.sentence[0].parent, s)
        self.assertEqual(s._truth_row, s.truth_row)

    def test_init_with_inner_sentence(self):
        s = Sentence(['or', ['or', 'Fire', 'Ice'], 'Water'])
        s.truth_row = 'test'
        self.assertEqual(type(s.sentence[0]), Sentence)
        self.assertEqual(type(s.sentence[1]), Symbol)
        self.assertEqual(s.sentence[0].parent, s)
        self.assertEqual(s.sentence[0].truth_row, 'test')

    def test_getting_truth_value(self):
        s = Sentence(['or', 'Fire', 'Ice'])
        s.truth_row = [True, False]
        self.assertTrue(s)


class TestSymbolClass(unittest.TestCase):

    def test_getting_truth_value(self):
        s = Sentence(['or', 'Fire', 'Ice'])
        s.truth_row = [True, False]
        self.assertTrue(s.sentence[0])
        self.assertFalse(s.sentence[1])


class TestModelCheck(unittest.TestCase):

    def test_basic_sentence(self):
        val = ModelCheck(['or', 'Fire', 'Ice'])
        self.assertEqual(val, Validity.satisfiable)

    def test_contradiction(self):
        val = ModelCheck(['and', ['not', 'Fire'], 'Fire'])
        self.assertEqual(val, Validity.unsatisfiable)

    def test_valid(self):
        val = ModelCheck(['or', ['not', 'Fire'], 'Fire'])
        self.assertEqual(val, Validity.valid)


class TextbookProblems(unittest.TestCase):

    def test_problem_a(self):
        val = ModelCheck(['=>', 'Smoke', 'Smoke'])
        self.assertEqual(val, Validity.valid)

    def test_problem_b(self):
        val = ModelCheck(['=>', 'Smoke', 'Fire'])
        self.assertEqual(val, Validity.satisfiable)

    def test_problem_c(self):
        val = ModelCheck(['=>', ['=>', 'Smoke', 'Fire'], ['=>', ['not', 'Smoke'], ['not', 'Fire']]])
        self.assertEqual(val, Validity.satisfiable)

    def test_problem_d(self):
        val = ModelCheck(['or', ['or', 'Smoke', 'Fire'], ['not', 'Fire']])
        self.assertEqual(val, Validity.valid)

    def test_problem_e(self):
        p = ['=>', ['and', 'Smoke', 'Heat'], 'Fire']
        q = ['or', ['=>', 'Smoke', 'Fire'], ['=>', 'Heat', 'Fire']]
        val = ModelCheck(['<=>', p, q])
        self.assertEqual(val, Validity.valid)

    def test_problem_f(self):
        p = ['=>', 'Smoke', 'Fire']
        q = ['=>', ['and', 'Smoke', 'Heat'], 'Fire']
        val = ModelCheck(['=>', p, q])
        self.assertEqual(val, Validity.valid)

    def test_problem_g(self):
        val = ModelCheck(['or', ['or', ['=>', 'Big', 'Dumb'], 'Dumb'], 'Big'])
        self.assertEqual(val, Validity.valid)


if __name__ == "__main__":
    unittest.main()
