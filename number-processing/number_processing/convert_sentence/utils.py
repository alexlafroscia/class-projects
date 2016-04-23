from functools import reduce


def combine_words_for_sentence(words, joiner=' '):
    def join_words(a, b):
        if b is not None and b != '':
            return a + joiner + b
        else:
            return a

    if len(words) == 0:
        return ''
    return reduce(join_words, words)
