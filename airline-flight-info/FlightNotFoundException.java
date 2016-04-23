/**
 * Flight Not Found Exception.
 * Custom exception type for signalling that the specified route was not
 * found.
 */
@SuppressWarnings("serial")
public class FlightNotFoundException extends Exception {

  public FlightNotFoundException() {}

  public FlightNotFoundException(String message) {
    super(message);
  }
}
