import pytest
from ngram.sentence_structure import Sentence


class TestSentenceClass:

    def setup_method(self, m):
        self.s = Sentence(['<s>', 'a', 'b', ',', 'b', 'b', 'a', 'c', '</s>'])

    def teardown_method(self, m):
        Sentence.word_counts = dict()
        self.s = None

    def test_check_for_equality_with_other_sentence(self):
        t = Sentence(['<s>', 'a', 'b', ',', 'b', 'b', 'a', 'c', '</s>'])
        assert self.s == t

        t = Sentence(['<s>', 'a', 'b', ',', 'c', '</s>'])
        assert self.s != t

    def test_check_for_equality_with_list(self):
        t = ['<s>', 'a', 'b', ',', 'b', 'b', 'a', 'c', '</s>']
        assert self.s == t

    def test_check_for_equality_with_string(self):
        assert self.s == 'a b, b b a c.'

    def test_representation_as_string(self):
        assert str(self.s) == 'a b, b b a c.'

    def test_error_when_replacing_without_training(self):
        with pytest.raises(RuntimeError):
            self.s.replace_words()


class TestReplaceWords:

    def setup_method(self, m):
        Sentence._reset()
        self.test_sentence = Sentence(['<s>', 'a', 'a', 'b', '</s>'])
        Sentence.replaced_words = True

    def teardown_method(self, m):
        self.test_sentence = None
        Sentence._reset()

    def test_one_training_method(self):
        r = Sentence(['<s>', 'a', 'b', '</s>'])
        assert r == 'a <unk>.'

    def test_replacing_unseen_word_in_test_data(self):
        r = Sentence(['<s>', 'a', 'j', '</s>'])
        assert r == 'a <unk>.'
