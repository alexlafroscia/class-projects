import java.util.Random;
import java.util.HashMap;
import java.math.BigInteger;

public class Substitute implements SymCipher {

  final int ARRAY_SIZE = 256;

  private byte[] key;

  private HashMap<Byte, Byte> decoderRing;

  /**
   * Used to keep track of which byte values have been put into the new array.
   */
  private boolean[] used;

  /**
   * Random number generator
   */
  private Random rand = new Random();

  public Substitute() {
    // Create the array
    this.key = new byte[ARRAY_SIZE];
    this.used = new boolean[ARRAY_SIZE];
    this.decoderRing = new HashMap<Byte, Byte>();

    // Populate it with byte values
    for (int i = 0; i < ARRAY_SIZE; i++) {
      byte unusedByte = this.getUnusedByteValue();
      this.key[i] = unusedByte;
      this.decoderRing.put(unusedByte, (byte)(i - 128));
    }
  }

  public Substitute(byte[] key) {
    System.out.println(key.length);
    // Create the array
    this.key = key;
    this.used = new boolean[ARRAY_SIZE];
    this.decoderRing = new HashMap<Byte, Byte>();

    for (int i = 0; i < ARRAY_SIZE; i++) {
      this.decoderRing.put(key[i], (byte)(i - 128));
    }
  }

  public byte[] getKey() {
    return this.key;
  }

  public byte[] encode(String s) {
    System.out.println("Encode:");
    System.out.println("Original message:            " + s);
    byte[] stringToBytes = s.getBytes();
    System.out.println("Bytes as BigInteger:         " + new BigInteger(1, stringToBytes));
    byte[] encodedArray = new byte[stringToBytes.length];
    for (int i = 0; i < stringToBytes.length; i++) {
      byte currentByte = stringToBytes[i];
      encodedArray[i] = this.key[currentByte + 128];
    }
    System.out.println("Encoded Bytes as BigInteger: " + new BigInteger(1, encodedArray));
    System.out.println();
    return encodedArray;
  }

  public String decode(byte[] bytes) {
    System.out.println("Decode:");
    System.out.println("Encoded Bytes as BigInteger: " + new BigInteger(1, bytes));
    byte[] decodedArray = new byte[bytes.length];
    for (int i = 0; i < bytes.length; i++) {
      decodedArray[i] = this.decoderRing.get(bytes[i]);
    }
    System.out.println("Bytes as BigInteger:         " + new BigInteger(1, decodedArray));
    String message = new String(decodedArray);
    System.out.println("Original message:            " + message);
    System.out.println();
    return message;
  }


  /**
   * Get a byte value that hasn't yet been inserted into the `key` array
   */
  private byte getUnusedByteValue() {
    int randomNum = this.getRandomNumber(0, ARRAY_SIZE - 1);

    // Try to get a random, possible byte value, then just iterate until a open
    // space is found.
    while (used[randomNum]) {
      randomNum = (randomNum + 1) % ARRAY_SIZE;
    }
    used[randomNum] = true;
    return (byte)(randomNum - (ARRAY_SIZE / 2));
  }


  /**
   * Get a random number
   *
   * @param min the minimum number in the range to select from
   * @param max the maximum number in the range to select from
   * @return the random number
   */
  private int getRandomNumber(int min, int max) {
    return this.rand.nextInt((max - min) + 1) + min;
  }
}

