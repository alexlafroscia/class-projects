from functools import reduce
from math import log, pow, inf
from statistics import mean


BASE = 2
JUMP = 0.05


def frange(x, y, jump):
    """
    Like `range()`, but for floats

    http://stackoverflow.com/a/7267280/2250435
    """
    while x < y:
        yield x
        x += jump


def trigram_lambdas():
    """
    Enumerate all lambdaA and lambdaB combinations for a trigram model

    Yields each possible value for (a) and (b) such that they do not exceed 1
    when added together
    """
    for a in frange(0, 1, JUMP):
        for b in frange(0, 1, JUMP):
            if (a + b) < 1:
                yield (a, b)


def find_negative_log(a):
    if a == 0:
        return a
    return -log(a, BASE)


def get_perplexity_from_probabilities(probabilities):
    """
    Combine a bunch of probabilties to get the entropy

    Arguments:
        probabilities (list(float)): probabilities to combine

    Return:
        (float): the entropy
    """
    modified_probabilities = map(find_negative_log, probabilities)
    entropy = reduce(lambda a, b: a + b, modified_probabilities, 0)
    entropy /= len(list(probabilities))
    return pow(BASE, entropy)


class ProceedingWord(object):
    """
    Store information about a proceeding word
    """

    def __init__(self, word, preceeding_words=None):
        self.word = word
        self.occurences = 0
        self.preceeding = preceeding_words

    @property
    def probability(self):
        return self.occurences / self.preceeding.total_occurences

    def __eq__(self, other):
        if isinstance(other, str):
            return self.word == other
        return self.word == other.word


class PreceedingWords(object):
    """
    Store infomation about a set of preceeding words and the words that came
    after them
    """

    def __init__(self, words):
        self.words = words
        self.proceeding_words = dict()
        self.total_occurences = 0

    def add_occurence(self, word):
        """
        Add another word to the occurences, adjusting the probability of all
        possible proceeding words based on the new one
        """
        if word not in self.proceeding_words:
            self.proceeding_words[word] = ProceedingWord(word, self)
        self.proceeding_words[word].occurences += 1
        self.total_occurences += 1

    @property
    def next_word(self):
        """
        Return the word that is most likely to be the next word, based on the
        set that are repesented by this object

        Returns:
            (ProceedingWord): the word that is most likely to be next
        """
        def highest_probability(a, b):
            if a.probability > b.probability:
                return a
            else:
                return b

        if len(self.proceeding_words) == 0:
            return None
        return reduce(highest_probability, self.proceeding_words.values())

    def __hash__(self):
        return hash(self.words)

    def __eq__(self, other):
        return hash(self) == hash(other)


class NGram(object):
    """
    NGram

    Stores information about the probability of some word occuring, given `N`
    preceeding words.

    In cases where we're doing a Unigram model, tracking 0 words historically,
    this structure continues to work by linking all words to an empty tuple of
    previous words.

    Arguments:
        - n (int): the number of historical words to base suggestions on
    """

    def __init__(self, n):
        self.n = n
        self.dictionary = dict()

    def add(self, word, preceeding=()):
        """
        Add a new preceeding words/next word combination to the data store

        If the preceeding tuple is not specified, the assumption will be made
        that we're doing a Unigram model and everything should be linked to
        an empty tuple.

        Arguments:
            word (string): The word to add
            preceeding_words (tuple): N number of preceeding words
        """
        self._ensure_preceeding(preceeding)
        self.dictionary[preceeding].add_occurence(word)

    def next_word(self, words=()):
        """
        Given some set of words, return the most likely next word

        Arguments:
            words (tuple): The previous words

        Returns:
            (string): the most likely next word
        """
        self._ensure_preceeding(words)
        return self.dictionary[words].next_word.word

    def probability_of(self, next_word, previous=()):
        try:
            return self.dictionary[previous] \
                .proceeding_words[next_word].probability
        except KeyError:
            return 0

    def _ensure_preceeding(self, preceeding):
        """
        Ensure that there is a dictionary entry for the preceeding word set
        """
        if preceeding not in self.dictionary:
            self.dictionary[preceeding] = PreceedingWords(preceeding)


class Model(object):

    def __init__(self, description):
        self.description = description
        self.unigram = NGram(0)
        self.bigram = NGram(1)
        self.trigram = NGram(2)

    @property
    def is_smoothed_bigram(self):
        return self.description == '2s'

    @property
    def is_smoothed_trigram(self):
        return self.description == '3s'

    def train(self, sentences):
        """
        Train the model on the given sentences

        Feed the given sentences to the NGrams, so that we can train the model
        on their structure.

        Arguments:
            sentences (list(Sentence)): the sentences to train against
        """
        if self.description == '1':
            self._unigram(sentences)
        if self.description == '2':
            self._bigram(sentences)
        if self.description == '2s':
            self._unigram(sentences)
            self._bigram(sentences)
        if self.description == '3':
            self._trigram(sentences)
        if self.description == '3s':
            self._unigram(sentences)
            self._bigram(sentences)
            self._trigram(sentences)

    def evaluate(self, sentences):
        """
        Evaluate some sentences based on the model, calculating their
        perplexity values

        Arguments:
            sentences (list(Sentence)): the sentences to evaluate

        Return:
            (list(float)): the corresponding perplexity values
        """
        perplexities = list()
        for sentence in sentences:
            couple = (sentence, self.perplexity_of(sentence))
            perplexities.append(couple)
        return perplexities

    def tune(self, sentences):
        if self.is_smoothed_bigram:
            self._tune_bigram(sentences)
        elif self.is_smoothed_trigram:
            self._tune_trigram(sentences)
        else:
            raise RuntimeError('Unexpected model type: {}'
                               .format(self.description))

    def _tune_bigram(self, sentences):
        best_lambda = None
        best_perplexity = inf
        for i in frange(0, 1, JUMP):
            self.lamA = i
            p = self._average_perplexity_for(sentences)
            if p < best_perplexity:
                best_perplexity = p
                best_lambda = i
        self.lamA = best_lambda
        print('Best Lambda A: {}'.format(self.lamA))

    def _tune_trigram(self, sentences):
        best_lambdas = (None, None)
        best_perplexity = inf
        for (a, b) in trigram_lambdas():
            self.lamA = a
            self.lamB = b
            p = self._average_perplexity_for(sentences)
            if p < best_perplexity:
                best_perplexity = p
                best_lambdas = (a, b)
        self.lamA = best_lambdas[0]
        self.lamB = best_lambdas[1]

    def _average_perplexity_for(self, sentences):
        d = self.evaluate(sentences)
        return mean(list(map(lambda couple: couple[1], d)))

    def perplexity_of(self, sentence):
        if self.description == '1':
            return self._unigram_perplexity_of(sentence)
        if self.description == '2':
            return self._bigram_perplexity_of(sentence)
        if self.description == '2s':
            uni = self._unigram_perplexity_of(sentence)
            bi = self._bigram_perplexity_of(sentence)
            return self._smooth(unigram=uni, bigram=bi)
        if self.description == '3':
            return self._trigram_perplexity_of(sentence)
        if self.description == '3s':
            uni = self._unigram_perplexity_of(sentence)
            bi = self._bigram_perplexity_of(sentence)
            tri = self._trigram_perplexity_of(sentence)
            return self._smooth(unigram=uni, bigram=bi, trigram=tri)

    def _unigram(self, sentences):
        """
        Run a Unigram on the given sentences

        Arguments:
            sentences (list(sentences)): the sentences to run against
        """
        for sentence in sentences:
            for word in sentence:
                self.unigram.add(word)

    def _bigram(self, sentences):
        """
        Run a Bigram on the given sentences

        Arguments:
            sentences (list(sentences)): the sentences to run against
        """
        for sentence in sentences:
            words = list(sentence)
            words.insert(0, '<pre>')
            for i in range(0, len(words) - 1):
                pre = words[i]
                post = words[i + 1]
                self.bigram.add(post, (pre))

    def _trigram(self, sentences):
        """
        Run a Trigram on the given sentences

        Arguments:
            sentences (list(sentences)): the sentences to run against
        """
        for sentence in sentences:
            words = list(sentence)
            words.insert(0, '<pre>')
            words.insert(0, '<pre>')
            for i in range(0, len(words) - 2):
                pre = words[i]
                pre2 = words[i + 1]
                post = words[i + 2]
                self.bigram.add(post, (pre, pre2))

    def _unigram_perplexity_of(self, sentence):
        """
        Find the unigram perplexity of a sentence

        Arguments:
            sentence (Sentence): the sentence to process

        Returns:
            (float): the perplexity
        """
        probabilities = list(map(lambda a: self.unigram.probability_of(a),
                             sentence))
        return get_perplexity_from_probabilities(probabilities)

    def _bigram_perplexity_of(self, sentence):
        """
        Find the bigram perplexity of a sentence

        Arguments:
            sentence (Sentence): the sentence to process

        Returns:
            (float): the perplexity
        """
        probabilities = list()
        words = list(sentence)
        words.insert(0, '<pre>')
        for i in range(0, len(sentence)):
            previous = words[i]
            current = words[i + 1]
            probabilities.append(self.bigram.probability_of(
                current, (previous)))
        return get_perplexity_from_probabilities(probabilities)

    def _trigram_perplexity_of(self, sentence):
        """
        Find the trigram perplexity of a sentence

        Arguments:
            sentence (Sentence): the sentence to process

        Returns:
            (float): the perplexity
        """
        probabilities = list()
        words = list(sentence)
        words.insert(0, '<pre>')
        words.insert(0, '<pre>')
        for i in range(0, len(sentence)):
            previous = words[i]
            previous2 = words[i + 1]
            current = words[i + 2]
            probabilities.append(self.bigram.probability_of(
                current, (previous, previous2)))
        return get_perplexity_from_probabilities(probabilities)

    def _smooth(self, unigram=None, bigram=None, trigram=None):
        """
        Smooth the perplexity of the sentence based on the provided parts

        Returns:
            (float): the smoothed perplexity value
        """
        if self.description == '2s':
            return self._smooth2(unigram, bigram)
        if self.description == '3s':
            return self._smooth3(unigram, bigram, trigram)
        raise Exception('Expected model to be smoothed; was {}'
                        .format(self.desription))

    def _smooth2(self, unigram, bigram):
        """
        Smooth a bigram model
        """
        return (self.lamA * unigram +
                (1 - self.lamA) * bigram)

    def _smooth3(self, unigram, bigram, trigram):
        """
        Smooth a trigram model
        """
        return (self.lamA * unigram +
                self.lamB * bigram +
                (1 - self.lamA - self.lamB) * trigram)
