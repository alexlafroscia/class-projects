"""
The cutoff value for word occurences when replacing
"""
K = 1


class Sentence(object):

    """
    Track the number of each type of word in our lexicon
    """
    word_counts = dict()

    """
    The token to use when replacing a low-count word with a "unknown word"
    marker
    """
    UNKNOWN_WORD_TOKEN = '<unk>'

    """
    Words to ignore when doing replacement
    """
    ignored_words = ['<s>', '</s>', '<unk>']

    """
    Whether or not the word counts has been finished
    """
    replaced_words = False

    def __init__(self, words):
        """
        Turn tokenized array of words into a sentence representation

        On initialization, if the replaced words have not yet been determined
        (meaning that the training sentences are still being read in), count
        the number of occurences of each word.

        Once the training data has finished being processed, the replaced words
        list will be determined.  After that point, any sentences will have
        words replaced automatically, so avoid the need to process them all
        again a second time later.
        """
        self.words = words
        # If we have not yet finished training the word count model, count the
        # words and keep track of this data
        if Sentence.replaced_words is False:
            for word in words:
                if word in Sentence.ignored_words:
                    continue
                if word not in Sentence.word_counts:
                    Sentence.word_counts[word] = 0
                Sentence.word_counts[word] += 1
        else:
            self.replace_words()

    def replace_words(self):
        if not Sentence.replaced_words:
            raise RuntimeError('Must finish building word replacement first')
        words = self.words
        for index, word in enumerate(words):
            if word in Sentence.ignored_words:
                continue
            try:
                if self.word_counts[word] <= K:
                    words[index] = Sentence.UNKNOWN_WORD_TOKEN
            except KeyError:
                words[index] = Sentence.UNKNOWN_WORD_TOKEN
        self.words = words

    def __iter__(self):
        for word in self.words:
            yield word

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise Exception('Must look up words by index')
        return self.words[index]

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        if isinstance(other, list):
            return hash(self) == hash(str(other))
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(str(self.words))

    def __str__(self):
        words = self.words[1:-1]
        string = ' '.join(words) + '.'
        return string.replace(' ,', ',')

    def __len__(self):
        return len(self.words)

    @classmethod
    def _reset(cls):
        """
        Reset the shared sentence state
        """
        cls.word_counts = dict()
        cls.replaced_words = None
