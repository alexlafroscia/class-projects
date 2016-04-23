/**
 * Print Service.
 * Collection of print methods
 */
import java.util.*;

public class PrintService {

  public PrintService() {}


  /**
   * Print a list of all the routes, without printing duplicates.
   * Duplicated routes are the reverse direction of a flight that has already
   * been acknowledged.
   *
   * @param map the map to print routes from
   * @param title the title to print for the table
   */
  public static void printFlightList(Graph map, String title) {
    int[][] printedList = new int[map.length + 1][map.length + 1];
    printFlightTableHeader(title);
    for (int i = 1; i <= map.length; i++) {
      Iterator<Edge> neighbors = map.flightsFor(i).iterator();
      while (neighbors.hasNext()) {
        Edge neighbor = neighbors.next();
        if (printedList[i][neighbor.id] == 0) {
          printedList[i][neighbor.id] = 1;
          printedList[neighbor.id][i] = 1;
          printFlightTableRow(map, i, neighbor);
        }
      }
    }
  }


  /**
   * Print the header of the flight table.
   *
   * @param header the string to print
   */
  public static void printFlightTableHeader(String header) {
    System.out.printf("\n%s\n\n", header);
    System.out.printf("| %-14s | %-14s | %-6s | %-7s |\n", "City 1",
                      "City 2", "Dist", "Price");
    System.out.println("------------------------------------------------------");
  }


  /**
   * Print a row of the flight table.
   *
   * @param map the map to get the city from
   * @param index the index to display for the row
   * @param id the ID number for the city to print
   * @param edge the edge to print information for
   */
  public static void printFlightTableRow(Graph map, int id, Edge edge) {
    String from = map.getCity(id).name;
    String to = map.getCity(edge.id).name;
    System.out.printf("| %14s | %14s | %6d | %7.2f |\n", from, to,
                      edge.distance, edge.price);
  }


  /**
   * Print the list of cities in the system with their ID numbers.
   *
   * @param map the map object to print from
   */
  public static void printCityList(Graph map) {
    for (int i = 1; i <= map.length; i++) {
      City city = map.getCity(i);
      System.out.printf("%3d. %s\n", city.id, city.name);
    }
  }
}

