# flake8: noqa

from number_processing.convert_sentence import transform, SubstituteObject


class TestSubstituteObject:

    def test_can_apply_transformation(self):
        sub = SubstituteObject('this is this input')

        def t(string):
            return 'this is the output'

        assert str(sub.apply_subtitution(t)) == 'this is the output'


class TestTransformFunction:

    def test_returns_string(self):
        result = transform('this is a test')
        assert isinstance(result, str)

    def test_result_contains_no_basic_numbers(self):
        result = transform('this number is 3')
        assert '3' not in result

    def test_replacing_dates(self):
        result = transform('January 10, 2015')
        assert result == 'January tenth, two thousand fifteen'

    def test_replacing_date_and_number(self):
        result = transform('January 10, 2015 2')
        assert result == 'January tenth, two thousand fifteen two'

    def test_replacing_multi_word_date(self):
        result = transform('January 29, 2015')
        assert result == 'January twenty ninth, two thousand fifteen'

    def test_replacing_fractions(self):
        result = transform('I have 3/4 of an apple.')
        assert result == 'I have three quarters of an apple.'


class TestCasesFromProfessor:

    def test_basic_examples(self):
        result = transform('A plain number like 1,234.567 .')
        assert result == 'A plain number like one thousand two hundred thirty four point five six seven .'
        result = transform('A date like January 15 , 2015 .')
        assert result == 'A date like January fifteenth, two thousand fifteen .'
        result = transform('A dollar amount like $ 3.25 .')
        assert result == 'A dollar amount like three dollars twenty five cents .'
        result = transform('A percentage like 0.35 % .')
        assert result == 'A percentage like zero point three five percent .'
        result = transform('A fraction like 7\/8 or 3 1\/2 .')
        assert result == 'A fraction like seven eighths or three and a half .'

    def test_made_up_examples(self):
        result = transform('An ordinal number like 42nd street , or 20th .')
        assert result == 'An ordinal number like forty second street , or twentieth .'
        result = transform('A large number without comma like 12345678.9123 .')
        assert result == 'A large number without comma like twelve million three hundred forty five thousand six hundred seventy eight point nine one two three .'
        result = transform('A large number with comma like 12,345,678.9123 .')
        assert result == 'A large number with comma like twelve million three hundred forty five thousand six hundred seventy eight point nine one two three .'
        result = transform('A dollar amount with names appended like $ 1.6 billion or $ 12.4 million .')
        assert result == 'A dollar amount with names appended like one point six billion dollars or twelve point four million dollars .'
        result = transform('A dollar amount with more than 2 digits in the cent part like $ 12.345 .')
        assert result == 'A dollar amount with more than two digits in the cent part like twelve dollars thirty four point five cents .'
        result = transform('A fractional percentage is 5 4\/6 % .')
        assert result == 'A fractional percentage is five and four sixths percent .'
        result = transform('A date without day like January , 2016 .')
        assert result == 'A date without day like January , two thousand sixteen .'
        result = transform('A date without year like January 14 .')
        assert result == 'A date without year like January fourteenth .'
        result = transform('A date with abbreviation like Jan 14 or Jan. 14 .')
        assert result == 'A date with abbreviation like January fourteenth or January fourteenth .'
        result = transform('A large dollar amount like $ 974.812 million or $ 974,812,000 .')
        assert result == 'A large dollar amount like nine hundred seventy four point eight one two million dollars or nine hundred seventy four million eight hundred twelve thousand dollars .'

    def test_real_sentences(self):
        result = transform('$ 150 million of 8.55 % senior notes due Oct. 15 , 2009 , priced at par .')
        assert result == 'one hundred fifty million dollars of eight point five five percent senior notes due October fifteenth, two thousand nine , priced at par .'
        result = transform('Sales amounted to $ 771.4 million , down 1.7 % from $ 784.9 million .')
        assert result == 'Sales amounted to seven hundred seventy one point four million dollars , down one point seven percent from seven hundred eighty four point nine million dollars .'
        result = transform('Weatherford currently has approximately 11.1 million common shares outstanding .')
        assert result == 'Weatherford currently has approximately eleven point one million common shares outstanding .'
        result = transform("Anticipating the Fed 's move , money traders lowered a key interest rate known as the Federal Funds rate to 8.625 % late Friday , down from 8.820 % the day before .")
        assert result == "Anticipating the Fed 's move , money traders lowered a key interest rate known as the Federal Funds rate to eight point six two five percent late Friday , down from eight point eight two zero percent the day before ."
        result = transform('On Oct. 16 , 1987 , the Nasdaq Composite fell 16.18 points , or 3.8 % , followed by its devastating 46.12-point , or 11 % slide , three days later .')
        assert result == 'On October sixteenth, nineteen eighty seven , the Nasdaq Composite fell sixteen point one eight points , or three point eight percent , followed by its devastating forty six point one two-point , or eleven percent slide , three days later .'
        result = transform('Lopid sales are expected to be about $ 300 million this year , up from $ 190 million in 1988 .')
        assert result == 'Lopid sales are expected to be about three hundred million dollars this year , up from one hundred ninety million dollars in nineteen eighty eight .'
        result = transform('Kollmorgen shares fell nearly 20 % on Friday to close at 12 7\/8 .')
        assert result == 'Kollmorgen shares fell nearly twenty percent on Friday to close at twelve and seven eighths .'
        result = transform('The Ginnie Mae November 9 % issue ended at 98 25\/32 , up 7\/8 point on the day , to yield about 9.28 % to a 12-year average life assumption .')
        assert result == 'The Ginnie Mae November ninth % issue ended at ninety eight and twenty five thirty seconds , up seven eighths point on the day , to yield about nine point two eight percent to a twelve-year average life assumption .'
        result = transform("Matsushita 's share in the venture will rise to 35 % Oct. 1 , 1990 , and to 50 % the following Oct. 1 .")
        assert result == "Matsushita 's share in the venture will rise to thirty five percent October first, nineteen ninety , and to fifty percent the following October first ."
        result = transform('Stocks : Volume 251,170,000 shares .')
        assert result == 'Stocks : Volume two hundred fifty one million one hundred seventy thousand shares .'
        result = transform('The Dow Jones industrials skidded 190.58 , to 2569.26 .')
        assert result == 'The Dow Jones industrials skidded one hundred ninety point five eight , to two thousand five hundred sixty nine point two six .'
        result = transform('The benchmark 30-year Treasury bond was quoted 6 p.m. EDT at 103 12\/32 , compared with 100 27\/32 Thursday , up 2 1\/2 points .')
        assert result == 'The benchmark thirty-year Treasury bond was quoted six p.m. EDT at one hundred three and twelve thirty seconds , compared with one hundred and twenty seven thirty seconds Thursday , up two and a half points .'
        result = transform('The interest-only securities were priced at 35 1\/2 to yield 10.72 % .')
        assert result == 'The interest-only securities were priced at thirty five and a half to yield ten point seven two percent .'
        result = transform('Beech Aircraft Corp. , a unit of Raytheon Co. , received an $ 11.5 million Air Force contract for C-12 aircraft support .')
        assert result == 'Beech Aircraft Corp. , a unit of Raytheon Co. , received an eleven point five million dollars Air Force contract for C-twelve aircraft support .'
