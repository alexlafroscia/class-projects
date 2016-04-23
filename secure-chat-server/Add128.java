import java.util.Random;
import java.math.BigInteger;

public class Add128 implements SymCipher {

  final int ARRAY_SIZE = 128;

  private byte[] key;

  private Random rand = new Random();

  public Add128() {
    // Create the array
    this.key = new byte[ARRAY_SIZE];

    // Populate it with random values
    for (int i = 0; i < ARRAY_SIZE; i++) {
      this.key[i] = getRandomByte(-127, 128);
    }
  }

  public Add128(byte[] key) {
    this.key = key;
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
      int index = i % ARRAY_SIZE;
      encodedArray[i] = (byte)(stringToBytes[i] + this.key[index]);
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
      int index = i % ARRAY_SIZE;
      decodedArray[i] = (byte)(bytes[i] - this.key[index]);
    }
    System.out.println("Bytes as BigInteger:         " + new BigInteger(1, decodedArray));
    String message = new String(decodedArray);
    System.out.println("Original message:            " + message);
    System.out.println();
    return message;
  }


  /**
   * Get a random number
   *
   * @param min the minimum number in the range to select from
   * @param max the maximum number in the range to select from
   * @return the random number
   */
  private byte getRandomByte(int min, int max) {
    return (byte)(this.rand.nextInt((max - min) + 1) + min);
  }
}

