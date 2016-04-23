import java.math.BigDecimal;


/**
 * A point on the map.
 */
public class Edge implements Comparable<Edge> {

  /**
   * The city ID for the adjoining city.
   */
  int id;


  /**
   * The city ID for the "starting" city.
   * Matches the ID in the adjacency list that corresponds to this list of
   * edges.
   */
  int originator;


  /**
   * The distance between the original and "to" cities.
   */
  int distance;


  /**
   * The property to make comparisons by.
   */
  private String comparator;


  /**
   * The price to travel between the two cities.
   */
  BigDecimal price;


  /**
   * Constructor.
   */
  public Edge(int id, int originator, int distance, BigDecimal price) {
    this.id = id;
    this.distance = distance;
    this.price = price;
    this.originator = originator;
    this.comparator = "distance";
  }


  /**
   * Given a vertex ID, return the other vertex ID for this edge.
   *
   * @param index one of the vertexes of this edge
   */
  public int other(int index) {
    int toReturn = 0;
    if (index == this.id) {
      toReturn = this.originator;
    } else if (index == this.originator) {
      toReturn = this.id;
    }
    return toReturn;
  }


  public void setComparator(String property) {
    this.comparator = property;
  }


  public int compareTo(Edge edge) {
    int toReturn = 0;
    if (this.comparator.equals("price")) {
      if (this.price.compareTo(edge.price) > 0) {
        toReturn = 1;
      } else if (this.price.compareTo(edge.price) < 0) {
        toReturn = -1;
      }
    } else {
      if (this.distance > edge.distance) {
        toReturn = 1;
      } else if (this.distance < edge.distance) {
        toReturn = -1;
      }
    }
    return toReturn;
  }

}
