from ngram import NGram, PreceedingWords, ProceedingWord, Model
from ngram.sentence_structure import Sentence


class TestNGramClass:

    def test_unigram(self):
        n = NGram(0)
        n.add('after')
        n.next_word() == 'after'

    def test_bigram(self):
        n = NGram(1)
        n.add('after', ('before'))
        assert n.next_word(('before')) == 'after'

    def test_trigram(self):
        n = NGram(2)
        n.add('after', ('before', 'other'))
        assert n.next_word(('before', 'other')) == 'after'


class TestPreceedingWordsClass:

    def test_next_word(self):
        p = PreceedingWords(('before'))
        p.add_occurence('after')
        p.add_occurence('after')
        p.add_occurence('other')
        assert p.next_word == 'after'

    def test_next_word_with_one(self):
        p = PreceedingWords(('before'))
        p.add_occurence('after')
        assert p.next_word == 'after'

    def test_next_word_with_zero(self):
        p = PreceedingWords(('before'))
        assert p.next_word is None

    def test_total_occurences(self):
        p = PreceedingWords(('before'))
        p.add_occurence('after')
        p.add_occurence('after')
        p.add_occurence('other')
        assert p.total_occurences == 3

    def test_total_occurences_when_zero(self):
        p = PreceedingWords(('before'))
        assert p.total_occurences == 0


class TestProceedingWordClass:

    def test_equality_with_word(self):
        assert ProceedingWord('before') == 'before'


class TestUnigramModel:

    def setup_method(self, test_method):
        self.m = Model('1')
        sentences = [
            Sentence(['<s>', 'a', 'b', '</s>']),
            Sentence(['<s>', 'a', 'b', '</s>'])
        ]
        self.m.train(sentences)

    def teardown_method(self, test_method):
        self.m = None
        self.sentences = None

    def test_training(self):
        n = self.m.unigram
        assert n.dictionary[()].proceeding_words['<s>'].probability == .25
        assert n.dictionary[()].proceeding_words['a'].probability == .25
        assert n.dictionary[()].proceeding_words['b'].probability == .25
        assert n.dictionary[()].proceeding_words['</s>'].probability == .25

    # def test_evaluation(self):
    #     sentence = Sentence(['<s>', 'a', 'b', '</s>'])
    #     result = self.m.evaluate([sentence])
    #     assert result[sentence] == 4.0
    #     sentence = Sentence(['<s>', 'b', 'a', '</s>'])
    #     result = self.m.evaluate([sentence])
    #     assert result[sentence] == 4.0
