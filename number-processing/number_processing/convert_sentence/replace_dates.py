import re
from .replace_numbers import replace_basic_numbers, convert_to_ordinal
from .utils import combine_words_for_sentence

date_regex = re.compile(
    r'(?P<month>\w+)(\.?)\s(?P<day>\d{1,2})(?P<year>\s?,?\s\d{4})?'
    )
misc_year_regex = re.compile('(?P<prefix>(?:in)|(?:to)|(?:from))' +
                             '\s(?P<year>\d{4}(?!\.\d))')


def replace_year(string):
    if len(string) != 4:
        raise Exception('Expected year to be 4 digits, was {}'
                        .format(len(string)))

    year = int(string)
    if year >= 2000:
        return replace_basic_numbers(year)
    else:
        arr = list(string)
        high_order = replace_basic_numbers(arr[0] + arr[1])
        low_order = replace_basic_numbers(arr[2] + arr[3])
        if low_order == 'zero':
            return high_order + ' hundred'
        if arr[2] == '0':
            low_order = 'oh ' + low_order
        return combine_words_for_sentence([high_order, low_order])


def convert_month(string):
    string = string.lower()
    if string.startswith('jan'):
        return 'January'
    if string.startswith('feb'):
        return 'February'
    if string.startswith('mar'):
        return 'March'
    if string.startswith('apr'):
        return 'April'
    if string.startswith('may'):
        return 'May'
    if string.startswith('jun'):
        return 'June'
    if string.startswith('jul'):
        return 'July'
    if string.startswith('aug'):
        return 'August'
    if string.startswith('sep'):
        return 'September'
    if string.startswith('oct'):
        return 'October'
    if string.startswith('nov'):
        return 'November'
    if string.startswith('dec'):
        return 'December'
    raise Exception('Unexpectd month input: {}'.format(string))


def date_replace(match):
    words = list()
    try:
        words.append(convert_month(match.group('month')))
    except:
        return match.group()

    # Replace day and suffix
    day = convert_to_ordinal(replace_basic_numbers(match.group('day')), False)

    if match.group('year') is not None:
        day += ','
    words.append(day)

    if match.group('year') is not None:
        year = replace_year(match.group('year').split(' ')[-1])
        words.append(year)

    # Join the broken string as a single string again
    return combine_words_for_sentence(words)


def parse_misc_years(string):
    def replace_misc_year(match):
        prefix = match.group('prefix')
        year = replace_year(match.group('year'))
        return combine_words_for_sentence([prefix, year])

    return misc_year_regex.sub(replace_misc_year, string)


def replace_dates(string):
    string = parse_misc_years(string)
    return date_regex.sub(date_replace, string)
