from number_processing.convert_sentence.replace_numbers import \
    number_to_words, create_number_stack, process_two_digit_number, \
    process_three_digit_number, process_comma_separated_number, \
    process_number, convert_to_ordinal


class TestCreateNumberStack:

    def test_it_works_for_small_numbers(self):
        result = create_number_stack(1)
        assert result[0] == 1

    def test_it_works_for_uneven_numbers(self):
        """Uneven numbers being those that are multiple of three digits"""
        result = create_number_stack(12345)
        assert result[0] == 345
        assert result[1] == 12

    def test_it_works_for_six_digit_numbers(self):
        result = create_number_stack(123456)
        assert result[0] == 456
        assert result[1] == 123


class TestProcessTwoDigitNumber:

    def test_it_works(self):
        result = process_two_digit_number(43)
        assert result == 'forty three'


class TestProcessThreeDigitNumber:

    def test_it_works(self):
        result = process_three_digit_number(143)
        assert result == 'one hundred forty three'


class TestCommaSeparatedNumbers:

    def test_it_works(self):
        result = process_comma_separated_number('123,450')
        assert result == 'one hundred twenty three thousand four hundred fifty'
        result = process_comma_separated_number('251,170,000')
        assert result == 'two hundred fifty one million one hundred ' + \
            'seventy thousand'

    def test_it_works_with_partial_high_order_place(self):
        result = process_comma_separated_number('12,340')
        assert result == 'twelve thousand three hundred forty'


class TestOrdinalNumbers:

    def test_one(self):
        assert convert_to_ordinal('one') == 'first'

    def test_two(self):
        assert convert_to_ordinal('two') == 'half'
        assert convert_to_ordinal('two', False) == 'second'

    def test_three(self):
        assert convert_to_ordinal('three') == 'third'

    def test_four(self):
        assert convert_to_ordinal('four') == 'quarter'
        assert convert_to_ordinal('four', False) == 'fourth'

    def test_five(self):
        assert convert_to_ordinal('five') == 'fifth'

    def test_six(self):
        assert convert_to_ordinal('six') == 'sixth'

    def test_seven(self):
        assert convert_to_ordinal('seven') == 'seventh'

    def test_eight(self):
        assert convert_to_ordinal('eight') == 'eighth'

    def test_nine(self):
        assert convert_to_ordinal('nine') == 'ninth'

    def test_twenty(self):
        assert convert_to_ordinal('twenty') == 'twentieth'

    def test_thirty(self):
        assert convert_to_ordinal('thirty') == 'thirtieth'

    def test_thirty_one(self):
        assert convert_to_ordinal('thirty one') == 'thirty first'


class TestNumbersWithDecimalPlaces:

    def test_it_works_for_regular_numbers(self):
        result = process_number('12.34')
        assert result == 'twelve point three four'
        result = process_number('12345.67')
        assert result == 'twelve thousand three hundred forty five point ' + \
            'six seven'
        result = process_number('2569.26')
        assert result == 'two thousand five hundred sixty nine point two six'

    def test_it_works_for_comma_separated_numbers(self):
        result = process_comma_separated_number('1,200.34')
        assert result == 'one thousand two hundred point three four'


class TestNumberToWords:

    def test_replacing_single_digit_numbers(self):
        assert number_to_words(0) == 'zero'
        assert number_to_words(1) == 'one'
        assert number_to_words(2) == 'two'
        assert number_to_words(3) == 'three'
        assert number_to_words(4) == 'four'
        assert number_to_words(5) == 'five'
        assert number_to_words(6) == 'six'
        assert number_to_words(7) == 'seven'
        assert number_to_words(8) == 'eight'
        assert number_to_words(9) == 'nine'

    def test_special_case_double_digit_numbers(self):
        assert number_to_words(10) == 'ten'
        assert number_to_words(11) == 'eleven'
        assert number_to_words(12) == 'twelve'
        assert number_to_words(13) == 'thirteen'
        assert number_to_words(14) == 'fourteen'
        assert number_to_words(15) == 'fifteen'
        assert number_to_words(16) == 'sixteen'
        assert number_to_words(17) == 'seventeen'
        assert number_to_words(18) == 'eighteen'
        assert number_to_words(19) == 'nineteen'
        assert number_to_words(20) == 'twenty'

    def test_normal_double_digit_numbers(self):
        assert number_to_words(21) == 'twenty one'
        assert number_to_words(30) == 'thirty'
        assert number_to_words(31) == 'thirty one'
        assert number_to_words(40) == 'forty'
        assert number_to_words(41) == 'forty one'
        assert number_to_words(50) == 'fifty'
        assert number_to_words(51) == 'fifty one'
        assert number_to_words(60) == 'sixty'
        assert number_to_words(61) == 'sixty one'
        assert number_to_words(70) == 'seventy'
        assert number_to_words(71) == 'seventy one'
        assert number_to_words(80) == 'eighty'
        assert number_to_words(81) == 'eighty one'
        assert number_to_words(90) == 'ninety'
        assert number_to_words(91) == 'ninety one'

    def test_three_digit_numbers(self):
        assert number_to_words(100) == 'one hundred'
        assert number_to_words(101) == 'one hundred one'
        assert number_to_words(200) == 'two hundred'
        assert number_to_words(201) == 'two hundred one'
        assert number_to_words(300) == 'three hundred'
        assert number_to_words(301) == 'three hundred one'
        assert number_to_words(400) == 'four hundred'
        assert number_to_words(401) == 'four hundred one'
        assert number_to_words(500) == 'five hundred'
        assert number_to_words(501) == 'five hundred one'
        assert number_to_words(600) == 'six hundred'
        assert number_to_words(601) == 'six hundred one'
        assert number_to_words(700) == 'seven hundred'
        assert number_to_words(701) == 'seven hundred one'
        assert number_to_words(800) == 'eight hundred'
        assert number_to_words(801) == 'eight hundred one'
        assert number_to_words(900) == 'nine hundred'
        assert number_to_words(901) == 'nine hundred one'

    def test_four_digit_numbers(self):
        assert number_to_words(1000) == 'one thousand'
        assert number_to_words(1001) == 'one thousand one'
        assert number_to_words(1101) == 'one thousand one hundred one'
        assert number_to_words(2000) == 'two thousand'
        assert number_to_words(3000) == 'three thousand'
        assert number_to_words(4000) == 'four thousand'
        assert number_to_words(5000) == 'five thousand'
        assert number_to_words(6000) == 'six thousand'
        assert number_to_words(7000) == 'seven thousand'
        assert number_to_words(8000) == 'eight thousand'
        assert number_to_words(9000) == 'nine thousand'

    def test_big_numbers(self):
        assert number_to_words(10000) == 'ten thousand'
        assert number_to_words(100000) == 'one hundred thousand'
        assert number_to_words(1000000) == 'one million'
        expected = 'one million one thousand one hundred one'
        assert number_to_words(1001101) == expected
        expected = 'one million one hundred one thousand one hundred'
        assert number_to_words(1101100) == expected
