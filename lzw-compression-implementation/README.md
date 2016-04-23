# LZW Implementation

##Goal:
To understand the innerworkings and implementation of the LZW compression algorithm, and to gain a better understanding of the performance it offers.

##High-level description:
As we discussed in lecture, LZW is a compression algorithm that was created in 1984 by Abraham Lempel, Jacob Ziv, and Terry Welch.
In its most basic form, it will output a compressed file as a series of fixed-length codewords.
This is the approach implemented in the LZW code provided by the authors of the textbook.
As we discussed in class, *variable-width* codewords can be used to increase the size of codewords output as the dictionary fills up.
Further, once the dictionary fills up, the algorithm can either stop adding patterns and continue compression with only the patterns already discovered, or the algorithm can reset the codebook to find new patterns.
The LZW code provided by the textbook authors simply continues to used patterns added to the codebook.

For this project, you will be modifying the LZW source code provided by the authors of the text book to use variable-width codewords, and to optionally reset the codebook under certain conditions.
With these changes in hand, you will then compare the performance of your modified LZW code with the provided LZW code, and further with the performance of a widely used compression application of your choice.
