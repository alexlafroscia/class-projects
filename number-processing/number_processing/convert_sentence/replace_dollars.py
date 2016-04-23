import re
from .replace_numbers import replace_basic_numbers, decimal_regex
from .utils import combine_words_for_sentence


dollar_sign_regex = '\$(?:\s?)'
modifier_regex = '(\s(?=\w))?(?P<modifier>\w*)'
dollar_regex = re.compile(r'' + dollar_sign_regex +
                          '(?P<amount>\d+)' + decimal_regex +
                          modifier_regex)
comma_seperated_dollar_regex = re.compile(r'' + dollar_sign_regex +
                                          '(?P<amount>\d{1,3},(\d{3},?)*)' +
                                          decimal_regex + modifier_regex)
modifiers = ['hundred', 'thousand', 'million', 'billion', 'trillion']


def convert_cents(string):
    cents = string.split('.')[1]
    if len(cents) > 2:
        cents = list(cents)
        cents.insert(2, '.')
        cents = ''.join(cents)
    return replace_basic_numbers(cents)


def dollar_replace(match):
    amount = match.group('amount')
    modifier = match.group('modifier')
    cents = match.group('decimal')
    words = list()

    if modifier in modifiers:
        if cents is None:
            amount = replace_basic_numbers(amount)
        else:
            amount = replace_basic_numbers(amount + cents)
        words.extend([amount, modifier, 'dollars'])
    else:
        amount = replace_basic_numbers(amount)
        words = [amount, 'dollars']
        if cents is not None:
            cents = convert_cents(cents)
            words.extend([cents, 'cents'])

    return combine_words_for_sentence(words)


def replace_dollars(string):
    string = str(string)  # Make sure that the input is actually a string
    string = comma_seperated_dollar_regex.sub(dollar_replace, string)
    return dollar_regex.sub(dollar_replace, string)
