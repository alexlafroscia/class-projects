/**
 * Helper Class for RSA Encryption.
 *
 * Wraps the math behind computing the ciphertext for a given message.
 * While it's not that much shorter of a syntax than doing the math directly in
 * the SecureChatClient, it's far more readable code.
 */
import java.math.BigInteger;

public class RSAHelper {

  //////// Class Methods ////////

  /**
   * Create the encrypted version of a BigInteger
   */
  public static BigInteger encrypt(BigInteger e, BigInteger n, BigInteger m) {
    return m.modPow(e, n);
  }


  //////// Instance Methods ////////

  private BigInteger e;
  private BigInteger n;

  public BigInteger encrypt(BigInteger m) {
    if (this.e == null || this.n == null) {
      return null;
    }
    return m.modPow(this.e, this.n);
  }

  public void setPubKey(BigInteger e) {
    this.e = e;
  }

  public void setModulus(BigInteger n) {
    this.n = n;
  }

}

