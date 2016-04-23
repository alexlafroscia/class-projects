from .replace_numbers import replace_basic_numbers
from .replace_dates import replace_dates
from .replace_dollars import replace_dollars
from .replace_fractions import replace_fractions


class SubstituteObject(object):

    def __init__(self, sentence):
        self.sentence = sentence

    def apply_subtitution(self, sub):
        """
        Apply some substitution function to the current sentence value

        Arguments:
            sub: A function that takes a string and returns another string.
            This should be used to apply a regex substitution to the current
            sentence value

        Returns:
            An instance of SubstituteObject, so that these substitution
            applications can be chained one after another
        """
        sentence = sub(self.sentence)
        self.sentence = sentence
        return self

    def __repr__(self):
        return self.sentence

    def __str__(self):
        return self.sentence


def transform(sentence):
    return SubstituteObject(sentence) \
        .apply_subtitution(replace_dates) \
        .apply_subtitution(replace_dollars) \
        .apply_subtitution(replace_fractions) \
        .apply_subtitution(replace_basic_numbers) \
        .sentence
