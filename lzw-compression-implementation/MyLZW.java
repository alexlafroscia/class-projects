/**
 * Custom LZW compression class.
 *
 * Compilation:  javac MyLZW.java
 * Execution:    java MyLZW - {@literal <} input.txt   (compress)
 * Execution:    java MyLZW + {@literal <} input.txt   (expand)
 * Dependencies: BinaryIn.java BinaryOut.java
 *
 * Compress or expand binary input from standard input using LZW.
 *
 * WARNING: STARTING WITH ORACLE JAVA 6, UPDATE 7 the SUBSTRING
 * METHOD TAKES TIME AND SPACE LINEAR IN THE SIZE OF THE EXTRACTED
 * SUBSTRING (INSTEAD OF CONSTANT SPACE AND TIME AS IN EARLIER
 * IMPLEMENTATIONS).
 *
 * See <a href = "http://java-performance.info/changes-to-string-java-1-7-0_06/">this article</a>
 * for more details.
 *
 * @author Alex LaFroscia
 */

public class MyLZW {

  /**
   * Number of characters by default.
   * A value of 256 represents EOF.
   */
  private static final int NUM_CHARS = 256;

  /**
   * The initial width of the codewords.
   */
  private static final int INITIAL_CODEWORD_WIDTH = 9;

  /**
   * The initial width of the codewords.
   */
  private static final int MAX_CODEWORD_WIDTH = 16;

  /**
   * The width of the codewords.
   * Represent the current width of the codewords being used.  Bound by
   * INITIAL_CODEWORD_WIDTH and MAX_CODEWORD_WIDTH.
   */
  private static int codewordWidth = INITIAL_CODEWORD_WIDTH;

  /**
   * The size of the original data.
   * Not simply the amount of data written out, since during compression the
   * data is read in and during expansion it is written out.
   */
  private static int numOriginalBits = 0;

  /**
   * The size of the compressed data.
   * Not simply the amount of data read in, since during compression the data is
   * written out and during expansion it is read in.
   */
  private static int numCompressedBits = 0;

  /**
   * Whether or not monitoring the compression ratio is turned on.
   */
  private static boolean isMonitoringCompressionRatio = false;

  /**
   * The original compression ratio to compare against.
   */
  private static float originalCompressionRatio;

  /**
   * Compress STDIn and pass to STDOut.
   *
   * @param compressionType which type of compression to perform
   */
  public static void compress(char compressionType) {
    String input = BinaryStdIn.readString();
    TST<Integer> codebook = new TST<Integer>();
    // Initialize the codebook with the 256 ASCII values
    for (int i = 0; i < NUM_CHARS; i++) {
      codebook.put("" + (char) i, i);
    }
    int code = NUM_CHARS + 1;  // NUM_CHARS is codeword for EOF

    // Write the compression type to the output
    switch(compressionType) {
      case 'n':
        BinaryStdOut.write(0, 2);
        break;
      case 'r':
        BinaryStdOut.write(1, 2);
        break;
      case 'm':
        BinaryStdOut.write(2, 2);
        break;
    }

    while (input.length() > 0) {

      // Find the longest prefix of the current input string that exists in the
      // codebook
      String s = codebook.longestPrefixOf(input);
      // Write the encoding for that prefix to STDOut
      BinaryStdOut.write(codebook.get(s), codewordWidth);
      numCompressedBits += codewordWidth;

      // Get the length of the prefix
      int t = s.length();
      numOriginalBits += t * 8;

      // Try adding to the codebook
      if (code == getNumCodewords() & canEmbiggenCodeword()) {
        // If the current number of codewords matches the amount we can store
        // based on the length of the codewords, and the codewords can be made
        // bigger, make them bigger.
        embiggenCodeword();
      } else if (code == getNumCodewords() & compressionType == 'r') {
        // If the current number of codewords matches the amount we can store,
        // but we _can't_ embiggen the codewords anymore, _and_ we're in reset
        // mode, then we can preform the reset logic
        codebook = resetCompression();
        code = NUM_CHARS + 1;
      } else if (code == getNumCodewords() & compressionType == 'm'
                 & !isMonitoringCompressionRatio) {
        isMonitoringCompressionRatio = true;
        originalCompressionRatio = getCompressionRatio();
      }

      // Check compression ratio if need be
      if (compressionType == 'm' & isMonitoringCompressionRatio) {
        if ((originalCompressionRatio / getCompressionRatio()) > 1.1) {
          codebook = resetCompression();
          code = NUM_CHARS + 1;
          isMonitoringCompressionRatio = false;
        }
      }

      // If the substring length is less than that of the entire that is left,
      // and the codebook isn't full, add another codeword
      if (t < input.length() && code < getNumCodewords()) {
        codebook.put(input.substring(0, t + 1), code++);
      }

      // Remove the prefix that we just encoded from the input string and repeat
      input = input.substring(t);            // Scan past s in input.
    }

    // Write NUM_CHARS to the file, to signify EOFj
    BinaryStdOut.write(NUM_CHARS, codewordWidth);
    numCompressedBits += codewordWidth;
    BinaryStdOut.close();
  }

  /**
   * Expand STDIn and pass to STDOut.
   */
  public static void expand() {
    String[] codebook = resetExpansion();
    int codewordValue = NUM_CHARS + 1;

    int compressionTypeBinary = BinaryStdIn.readInt(2);
    char compressionType = '\0';
    switch(compressionTypeBinary) {
      case 0:
        compressionType = 'n';
        break;
      case 1:
        compressionType = 'r';
        break;
      case 2:
        compressionType = 'm';
        break;
      default:
        System.err.println("There was a problem determining the compression method");
        System.exit(1);
    }

    int codeword = BinaryStdIn.readInt(codewordWidth);
    numCompressedBits += codewordWidth;

    if (codeword == NUM_CHARS) return; // expanded message is empty string
    String val = codebook[codeword];

    while (true) {
      // Write the value for the current code
      BinaryStdOut.write(val);
      numOriginalBits += val.length() * 8;

      // Embiggen the codeword, if necessary, and make the array bigger too
      if (codewordValue == getNumCodewords() & canEmbiggenCodeword()) {
        String[] biggerCodebook = new String[getNumCodewords() * 2];
        for(int i = 0; i < getNumCodewords(); i++) {
          biggerCodebook[i] = codebook[i];
        }
        codebook = biggerCodebook;
        embiggenCodeword();
      } else if (codewordValue == getNumCodewords() & compressionType == 'r') {
        codebook = resetExpansion();
        codewordValue = NUM_CHARS + 1;
      } else if (codewordValue == getNumCodewords() & compressionType == 'm'
                 & !isMonitoringCompressionRatio) {
        isMonitoringCompressionRatio = true;
        originalCompressionRatio = getCompressionRatio();
      }

      // Check compression ratio if need be
      if (compressionType == 'm' & isMonitoringCompressionRatio) {
        if ((originalCompressionRatio / getCompressionRatio()) > 1.1) {
          codebook = resetExpansion();
          codewordValue = NUM_CHARS + 1;
          isMonitoringCompressionRatio = false;
        }
      }

      // Get the next codeword from the input
      codeword = BinaryStdIn.readInt(codewordWidth);
      numCompressedBits += codewordWidth;

      // 256 marks EOF, exit
      if (codeword == NUM_CHARS) break;

      // Get the value for the current codeword
      String s = codebook[codeword];

      if (codewordValue == codeword) s = val + val.charAt(0);   // special case hack
      if (codewordValue < getNumCodewords()) codebook[codewordValue++] = val + s.charAt(0);
      val = s;
    }
    BinaryStdOut.close();
  }

  /**
   * Run the compression or expansion algorithm
   *
   * @param args command line arguments
   */
  public static void main(String[] args) {
    // If compression or expansion isn't specified, exit
    if (args.length == 0) {
      System.err.println("You need to specify compression or expansion");
      System.exit(1);
    }

    if (args[0].equals("-")) {
      // If the compression mode isn't just a character, exit
      if (args[1].length() > 1) {
        System.err.println("Invalid compression mode");
        System.exit(1);
      }
      // Convert the one-character second argument to a character
      char compressionType = args[1].charAt(0);
      switch (compressionType) {
        case 'n':
        case 'r':
        case 'm':
          // Run the compression, passing in the correct compression type
          compress(compressionType);
          break;
        default:
          // If the compression type is not one of the accepted types, exit
          System.err.println("Please specify a compression mode");
          System.exit(1);
      }
    } else if (args[0].equals("+")) {
      expand();
    } else {
      System.err.println("Illegal command line argument");
      System.exit(1);
    }
  }

  /**
   * Can the codeword be embiggened?
   */
  private static boolean canEmbiggenCodeword() {
    return codewordWidth < MAX_CODEWORD_WIDTH;
  }

  /**
   * Embiggen Codeword.
   * Incrememnts the size of the codeword, up until it reaches the maximum
   * value.
   *
   * @return whether or not the embiggening was successful
   */
  private static boolean embiggenCodeword() {
    if (canEmbiggenCodeword()) {
      codewordWidth++;
      return true;
    } else {
      return false;
    }
  }

  /**
   * Get Num Codewords.
   * Calculates and returns the number of codewords based on the number of
   * characters available and codeword width.  Replaces the property that used
   * to contain the same value.
   */
  private static int getNumCodewords() {
    return (int) Math.pow(2, codewordWidth);
  }

  /**
   * Reset the compression algorithm.
   * Returns a codebook with only the basic ASCII characters in it, as well as
   * resets the codeword width back to 9
   */
  private static TST<Integer> resetCompression() {
    // Reset the size of the codewords
    codewordWidth = INITIAL_CODEWORD_WIDTH;
    // Reset the codebook
    TST<Integer> codebook = new TST<Integer>();
    for (int i = 0; i < NUM_CHARS; i++) {
      codebook.put("" + (char) i, i);
    }
    return codebook;
  }

  /**
   * Reset the expansion algorithm.
   */
  private static String[] resetExpansion() {
    // Reset the size of the codewords
    codewordWidth = INITIAL_CODEWORD_WIDTH;
    // Set up an empty codebook with enough space for the codewords, based on
    // the default width
    String[] emptyCodebook = new String[getNumCodewords()];
    int codewordValue;
    for (codewordValue = 0; codewordValue < NUM_CHARS; codewordValue++) {
      emptyCodebook[codewordValue] = "" + (char) codewordValue;
    }
    emptyCodebook[codewordValue++] = "";
    return emptyCodebook;
  }

  /**
   * Get the current compression ratio.
   * Returns the compression ratio by dividing the number of "original" bits by
   * the number of compressed bits.
   */
  private static float getCompressionRatio() {
    return (float) numOriginalBits / (float) numCompressedBits;
  }

}
