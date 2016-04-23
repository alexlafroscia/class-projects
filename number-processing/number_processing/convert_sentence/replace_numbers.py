import re
from .utils import combine_words_for_sentence


percentage_regex = '(?P<percent>\s?\%)?'
decimal_regex = '(?P<decimal>\.(?:\d+))?'
ordinal_regex = '(?P<ordinal>(?:st)|(?:rd)|(?:th)|(?:nd))?'
basic_number_regex = re.compile(r'(?P<number>\d+)' + decimal_regex +
                                ordinal_regex + percentage_regex)
comma_seperated_number_regex = re.compile(r'(?P<number>\d{1,3},(\d{3},?)*)' +
                                          decimal_regex)


def create_number_stack(number):
    """
    Takes an number and returns an array of digits, grouped into threes, from
    lowest to highest

    This is used to grab each "place" grouping (hundreds, thousands, millions,
    etc) in lowest to highest order, so that they can be processed from lowest
    to highest significance.

    Arguments:
        int: the number to process

    Returns:
        list: the stack of 3 (or less)-digit numbers
    """
    stack = list()
    temp = list(str(number))

    while (len(temp) > 3):
        high = temp.pop()
        middle = temp.pop()
        low = temp.pop()
        combined_number = int(''.join([low, middle, high]))
        stack.append(combined_number)

    combined_number = int(''.join(temp))
    stack.append(combined_number)

    return stack


def process_two_digit_number(number):
    """
    For some 2-digit number, return the corresponding "words"
    """
    number = int(number)  # Convert to number, in case it isn't for some reason

    if (number < 20):
        return process_special_two_digit_number(number)

    [tens_place, ones_place] = map(lambda x: int(x), list(str(number)))
    if (tens_place == 2):
        tens_place = 'twenty'
    elif (tens_place == 3):
        tens_place = 'thirty'
    elif (tens_place == 4):
        tens_place = 'forty'
    elif (tens_place == 5):
        tens_place = 'fifty'
    elif (tens_place == 6):
        tens_place = 'sixty'
    elif (tens_place == 7):
        tens_place = 'seventy'
    elif (tens_place == 8):
        tens_place = 'eighty'
    elif (tens_place == 9):
        tens_place = 'ninety'
    else:
        raise Exception('Unexpected tens place, was {}. Value was {}'
                        .format(tens_place, number))

    if (ones_place == 0):
        return tens_place
    return ' '.join([tens_place, process_special_two_digit_number(ones_place)])


def process_special_two_digit_number(number, include_zero=False):
    """
    Since all of the numbers less than 20 have to be handled individually, we
    can pull their processing out into its own function

    Arguments:
        int: the number to convert

    Returns:
        string: the word equivalent
    """
    number = int(number)

    if (number == 0):
        if include_zero:
            return 'zero'
        else:
            return ''
    if (number == 1):
        return 'one'
    elif (number == 2):
        return 'two'
    elif (number == 3):
        return 'three'
    elif (number == 4):
        return 'four'
    elif (number == 5):
        return 'five'
    elif (number == 6):
        return 'six'
    elif (number == 7):
        return 'seven'
    elif (number == 8):
        return 'eight'
    elif (number == 9):
        return 'nine'
    elif (number == 10):
        return 'ten'
    elif (number == 11):
        return 'eleven'
    elif (number == 12):
        return 'twelve'
    elif (number == 13):
        return 'thirteen'
    elif (number == 14):
        return 'fourteen'
    elif (number == 15):
        return 'fifteen'
    elif (number == 16):
        return 'sixteen'
    elif (number == 17):
        return 'seventeen'
    elif (number == 18):
        return 'eighteen'
    elif (number == 19):
        return 'nineteen'
    else:
        raise Exception('Unexpected value: {}'.format(number))


def process_three_digit_number(number):
    number_string = str(number)
    number_string_length = len(number_string)
    if (number_string_length > 3):
        raise Exception('Expected length of number to be 3 or fewer, was {}'
                        .format(len(number_string)))
    elif (number_string_length == 1 or number_string_length == 2):
        return process_two_digit_number(number)

    string_prefix = process_two_digit_number(int(number_string[0])) \
        + ' hundred'
    string_suffix = process_two_digit_number(
        int(number_string[1] + number_string[2]))
    return combine_words_for_sentence([string_prefix, string_suffix])


def translate_index_to_value_classifier(number):
    if (number == 0):
        return None
    elif (number == 1):
        return 'thousand'
    elif (number == 2):
        return 'million'
    elif (number == 3):
        return 'billion'
    elif (number == 4):
        return 'trillion'


def number_to_words(number):
    if number == 0:  # Special-case '0' b/c you usually want to leave it out
        return 'zero'
    stack = create_number_stack(number)
    return process_number_stack(stack)


def process_number_stack(stack):
    words = list()
    for i in range(len(stack)):
        val = stack[i]
        if val == 0 or val == '0' or val == '000':
            continue
        val = process_three_digit_number(val)
        classifier = translate_index_to_value_classifier(i)
        if classifier:
            val += ' ' + classifier
        words.insert(0, val)
    return combine_words_for_sentence(words)


def process_comma_separated_number(string):
    def replace_comma_separated_numbers(match):
        value = match.group('number')
        if value == '':
            return ''
        array = value.split(',')
        array.reverse()
        return combine_words_for_sentence([
            process_number_stack(array),
            process_decimal_places(match.group('decimal'))
            ])

    return comma_seperated_number_regex.sub(
        replace_comma_separated_numbers, string)


def convert_to_ordinal(string, fraction=True):
    # Special case two, because "32" should not become "thirty half"
    if string == 'two' and fraction:
        return 'half'
    if string == 'four' and fraction:
        return 'quarter'

    words = string.split(' ')
    last = words.pop()
    if last == 'one':
        last = 'first'
    elif last == 'two':
        last = 'second'
    elif last == 'three':
        last = 'third'
    elif last == 'four':
        last = 'fourth'
    elif last == 'five':
        last = 'fifth'
    elif last == 'eight':
        last = 'eighth'
    elif last == 'nine':
        last = 'ninth'
    elif last == 'twelve':
        last = 'twelfth'
    elif last == 'twenty':
        last = 'twentieth'
    elif last == 'thirty':
        last = 'thirtieth'
    else:
        last = last + 'th'
    words.append(last)
    return combine_words_for_sentence(words)


def process_number(string):
    return basic_number_regex.sub(num_replace, string)


def process_decimal_places(string):
    if string == '' or string is None:
        return ''
    numbers = string.split('.')[1]
    words = list()
    for char in list(numbers):
        word = process_special_two_digit_number(char, True)
        words.append(word)
    words.insert(0, 'point')
    return combine_words_for_sentence(words)


def num_replace(match):
    value = number_to_words(int(match.group('number')))
    words = list()

    if match.group('ordinal'):
        value = convert_to_ordinal(value)
    words.append(value)

    words.append(process_decimal_places(match.group('decimal')))

    if match.group('percent') is not None:
        words.append('percent')

    return combine_words_for_sentence(words)


def replace_basic_numbers(string):
    string = str(string)  # Make sure that the input is actually a string
    string = process_comma_separated_number(string)
    return process_number(string)
