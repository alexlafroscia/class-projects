from number_processing.convert_sentence.replace_fractions import \
    replace_fractions


class TestReplaceFractions:

    def test_replace_fractions(self):
        result = replace_fractions('1000/102')
        assert result == 'one thousand one hundred seconds'

    def test_replace_fractions_with_spaces(self):
        result = replace_fractions('10 / 12')
        assert result == 'ten twelfths'
        result = replace_fractions('69 / 32')
        assert result == 'sixty nine thirty seconds'

    def test_replace_factions_without_spaces(self):
        result = replace_fractions('10/12')
        assert result == 'ten twelfths'
        result = replace_fractions('69/32')
        assert result == 'sixty nine thirty seconds'

    def test_replace_special_fractions(self):
        result = replace_fractions('1/2')
        assert result == 'a half'
        result = replace_fractions('2/3')
        assert result == 'two thirds'
        result = replace_fractions('3/4')
        assert result == 'three quarters'
        result = replace_fractions('4/5')
        assert result == 'four fifths'
        result = replace_fractions('5/6')
        assert result == 'five sixths'

    def test_backslash(self):
        result = replace_fractions('1\/2')
        assert result == 'a half'

    def test_replace_fractions_with_prefix(self):
        result = replace_fractions('7 3/4')
        assert result == 'seven and three quarters'
