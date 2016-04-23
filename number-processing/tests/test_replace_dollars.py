from number_processing.convert_sentence.replace_dollars import replace_dollars


class TestReplaceDollars:

    def test_replace_dollars_without_modifier(self):
        assert replace_dollars('$10') == 'ten dollars'
        assert replace_dollars('$100') == 'one hundred dollars'

    def test_replace_dollars_with_space_before_sign(self):
        assert replace_dollars('$ 10') == 'ten dollars'
        assert replace_dollars('$ 1000') == 'one thousand dollars'

    def test_replace_dollars_with_modifier(self):
        assert replace_dollars('$1 hundred') == 'one hundred dollars'
        result = replace_dollars('$100 thousand')
        assert result == 'one hundred thousand dollars'
        result = replace_dollars('$100 million')
        assert result == 'one hundred million dollars'
        result = replace_dollars('$100 billion')
        assert result == 'one hundred billion dollars'
        result = replace_dollars('$100 trillion')
        assert result == 'one hundred trillion dollars'

    def test_modifier_with_decimal_place(self):
        result = replace_dollars('$1.6 billion')
        assert result == 'one point six billion dollars'
        result = replace_dollars('$ 1.6 billion')
        assert result == 'one point six billion dollars'

    def test_with_multiple_dollar_amounts(self):
        result = replace_dollars('$1.6 billion or $1.2 million')
        assert result == 'one point six billion dollars or one point two ' + \
            'million dollars'


class TestReplaceDollarsAndCents:

    def test_it_works(self):
        assert replace_dollars('$10.25') == 'ten dollars twenty five cents'


def test_it_does_not_consume_trailing_whitespace():
    assert replace_dollars('$10.15 .') == 'ten dollars fifteen cents .'
