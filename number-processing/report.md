# Report: Number Substitution

## Supported Types and Variations

**Basic Numbers**

My program supports basic numbers as suggested by the basic requirement set, both with and without commas separating the different segments of the number.  Both cases also support decimal places and will convert those to English correctly.

**Dates**

Support for full dates, like *January 10, 2015* are supported, as well as abbreviations of the Month both using a period after the abbreviation or not.  In addition, parsing instances of dates without the year is supported as well.  Years without a mention of date it supported in many cases, but relies on a little bit of sentence context to achieve that; since I decided to support non-comma-separated numbers, these two cases conflict with one another sometimes.

When parsing a year, for the most part the two high-order and low-order digits are "pronounced" separately, so *1985* becomes "nineteen eighty five".  The exception to this is the 2000s, which are converted as "two thousand" instead.  Additionally, years that end on *0X* are converted as "oh X" to match the way they would be said aloud.

**Dollar Ammounts**

Dollar amounts are supported, both with and without commas segmenting the number.  Decimal values are correctly converted to cents, and three-or-more digit decimals are converted to be some partial cent value, like *$1.005* becoming "one dollar point five cents".

**Percentages**

Percentages are correctly handled.  Since this category overlapped a lot with others, it is is really not expanded on in and of itself.  However, fractional percentages are supported and parsed correctly.

**Fractions**

Fractions are supported, and convert the denominator to the ordinal version of the number specified.  The denominator will also be pluralized based on the value of the numerator.  In addition, care was taken to convert fractions over two or four into halves and quarters, respectively.

In addition to supporting fractions where the slash is escaped, I also support un-escaped slashes, as well as spaces or no spaced between the numbers and the slash.


## Identifying Variations

I built out a fairly extensive test suite (included in the submitted source code, runnable using `py.test`) that helped me verify all of the possible inputs and check that they were handled to my satisfaction.  Aside from building out my tests, however, I tried to identify common ways that you might modify a pattern.  For example, whitespace within any of the patterns is almost always optional, and regular expressions generally make it fairly easy to deal with that fact.

Part of what helped me be flexible in my matching was the fact that I made extensive use of named groups in the regular expressions, as well as making these groups optional.  For example, I would match the Year specifically within the expression for matching dates, and allow for matches that did not include the year.  In my substitution function, I would check for the existence of that particular part of the match and handle modifying the output accordingly.  This made handling situations where parts of a match were missing really easy.


## Difficulties

Having not spent that much time in the past working with regular expressions, this project made me realize that they are pretty eager to consume more of the sentence than you want them too.  For example, some of the patterns would often consume whitespace when I didn't want them to, especially at the end of the sentence.  This required the patterns to be updated to use lookaheads in determining whether or not to read in some whitespace, which helped to prevent more of it from being consumed than I intended.

Honestly, I feel like regular expressions are a fine tool for doing this kind of work, although something that was able to understand context a bit more would certainly help in certain cases.  As I mentioned previously, once case that is hard to differentiate is the occurrence of a pattern like "in 1960".  It's completely ambiguous to a program that cannot glean a greater context from the sentence where we're talking about the year 1960 or talking about, for example, a one in 1960 chance of an event taking place.  However, for the most part I was really impressed with how well regular expressions were able to handle the task of parsing out the dates and replacing them with the correct substitution, without knowing a greater context for the text being processed.
