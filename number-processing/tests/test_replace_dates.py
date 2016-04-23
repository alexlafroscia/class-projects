from number_processing.convert_sentence.replace_dates import replace_dates, \
    replace_year


class TestReplacingYear:

    def test_replace_year(self):
        assert replace_year('1492') == 'fourteen ninety two'
        assert replace_year('2000') == 'two thousand'
        assert replace_year('1999') == 'nineteen ninety nine'
        assert replace_year('2010') == 'two thousand ten'
        assert replace_year('1905') == 'nineteen oh five'


class TestReplacingDates:

    def test_replacing_two_dates(self):
        result = replace_dates('January 10, 2015 and January 11, 2015')
        assert result == 'January tenth, two thousand fifteen and January ' + \
            'eleventh, two thousand fifteen'

    def test_year_1500(self):
        result = replace_dates('January 10, 1500')
        assert result == 'January tenth, fifteen hundred'
        result = replace_dates('January 5, 1510')
        assert result == 'January fifth, fifteen ten'

    def test_year_1600(self):
        assert replace_dates('February 10, 1600') == 'February tenth,' + \
            ' sixteen hundred'
        assert replace_dates('October 5, 1610') == 'October fifth, sixteen ten'

    def test_year_1700(self):
        result = replace_dates('January 10, 1700')
        assert result == 'January tenth, seventeen hundred'
        result = replace_dates('January 5, 1710')
        assert result == 'January fifth, seventeen ten'

    def test_year_1800(self):
        result = replace_dates('December 25, 1800')
        assert result == 'December twenty fifth, eighteen hundred'
        result = replace_dates('November 5, 1892')
        assert result == 'November fifth, eighteen ninety two'

    def test_year_1900(self):
        result = replace_dates('June 2, 1900')
        assert result == 'June second, nineteen hundred'
        result = replace_dates('December 31, 1999')
        assert result == 'December thirty first, nineteen ninety nine'

    def test_year_2000(self):
        result = replace_dates('January 5, 2000')
        assert result == 'January fifth, two thousand'
        result = replace_dates('September 28, 2004')
        assert result == 'September twenty eighth, two thousand four'
        result = replace_dates('March 7, 2016')
        assert result == 'March seventh, two thousand sixteen'


class TestTransformingMonth:

    def test_it_works(self):
        result = replace_dates('Jan. 10, 1999')
        assert result == 'January tenth, nineteen ninety nine'


class TestMiscYears:

    def test_in(self):
        result = replace_dates('in 1999')
        assert result == 'in nineteen ninety nine'

    def test_from_to(self):
        result = replace_dates('from 1500 to 1600')
        assert result == 'from fifteen hundred to sixteen hundred'


class TestDatesWithoutYears:

    def test_it_works(self):
        result = replace_dates('Jan. 10')
        assert result == 'January tenth'

    def test_it_does_not_consume_trailing_whitespace(self):
        result = replace_dates('November 9 ')
        assert result == 'November ninth '
