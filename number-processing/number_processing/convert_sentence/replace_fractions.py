import re
from .replace_numbers import replace_basic_numbers, convert_to_ordinal, \
    percentage_regex
from .utils import combine_words_for_sentence


fraction_regex = re.compile(r'(?P<prefix>\d*?)(?:(?<=\d)\s*)?' +
                            '(?P<numerator>\d+)\s?\\\?\/\s?' +
                            '(?P<denominator>\d+)' +
                            percentage_regex)


def replace_custom_numerator(num):
    if num == 'one':
        return 'a'
    else:
        return num


def pluralize_denominator(num, denom):
    if num == 'a':
        return denom
    if denom == 'half':
        return 'halves'
    return denom + 's'


def fraction_replace(match):
    prefix = replace_basic_numbers(match.group('prefix'))
    numerator = replace_basic_numbers(match.group('numerator'))
    denominator = replace_basic_numbers(match.group('denominator'))

    words = list()
    if prefix != '':
        words.append(prefix)
        words.append('and')

    numerator = replace_custom_numerator(numerator)
    denominator = convert_to_ordinal(denominator)
    denominator = pluralize_denominator(numerator, denominator)
    words.extend([numerator, denominator])

    if match.group('percent') is not None:
        words.append('percent')

    return combine_words_for_sentence(words)


def replace_fractions(string):
    string = str(string)
    return fraction_regex.sub(fraction_replace, string)
