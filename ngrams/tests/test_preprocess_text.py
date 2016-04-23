from ngram.preprocess_text import make_sentences, tokenize_sentence, \
    tokenize_text, split_preprocessed_text, tokenize_real_text
from ngram.sentence_structure import Sentence


class TestSplitPreprocessedText:

    def test_it_works(self):
        s = split_preprocessed_text('<s> a b </s>\n<s> b a </s>')
        assert s[0] == ['<s>', 'a', 'b', '</s>']
        assert s[1] == ['<s>', 'b', 'a', '</s>']


class TestMakeSentences:

    def test_handle_unprocessed_text(self):
        sentences = make_sentences('a b b a. b a b b.')
        assert sentences[0] == 'a b b a.'
        assert sentences[1] == 'b a b b.'
        for sentence in sentences:
            assert isinstance(sentence, Sentence)

    def test_handle_multiline_text(self):
        s = make_sentences('a b b\na. b a b b.')
        assert s[0] == 'a b b a.'
        assert isinstance(s[0], Sentence)
        assert s[1] == 'b a b b.'
        assert isinstance(s[1], Sentence)

    def test_handle_processed_text(self):
        s = make_sentences('<s> a b b a </s>\n<s> b a b b </s>')
        assert s[0] == 'a b b a.'
        assert isinstance(s[0], Sentence)
        assert s[1] == 'b a b b.'
        assert isinstance(s[1], Sentence)

    def test_newline_at_end_of_file(self):
        s = make_sentences('<s> a b b a </s>\n<s> b a b b </s>\n')
        assert len(s) == 2

    def test_problematic_sentences(self):
        sentence = make_sentences('<s> a a , a b , b </s>')[0]
        assert sentence == 'a a, a b, b.'

    def test_real_text(self):
        sentences = make_sentences('''
            This is some real text.  It is pretty long, and has some
            stuff in it.  But that's cool, since we need to
            handle that.
        ''', True)
        assert str(sentences[0]) == 'This is some real text.'
        assert str(sentences[1]) == \
            'It is pretty long, and has some stuff in it.'
        assert str(sentences[2]) == \
            'But that\'s cool, since we need to handle that.'
        for sentence in sentences:
            assert isinstance(sentence, Sentence)
            assert sentence.words[0] == '<s>'
            assert sentence.words[len(sentence) - 1] == '</s>'


class TestTokenizeSentence:

    def test_toy_sentence(self):
        words = tokenize_sentence('a b a c a')
        assert words == ['<s>', 'a', 'b', 'a', 'c', 'a', '</s>']

    def test_it_spaces_out_commas(self):
        words = tokenize_sentence('a, b')
        assert words == ['<s>', 'a', ',', 'b', '</s>']

    def test_it_removed_excess_periods(self):
        words = tokenize_sentence('a b a c a.')
        assert words == ['<s>', 'a', 'b', 'a', 'c', 'a', '</s>']


class TestTokenizeText:

    def test_toy_text(self):
        matrix = tokenize_text('a b a b.\nb a b a.')
        assert matrix == [
            ['<s>', 'a', 'b', 'a', 'b', '</s>'],
            ['<s>', 'b', 'a', 'b', 'a', '</s>']
        ]
