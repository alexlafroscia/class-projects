import java.util.*;

public class DijkstraShortestPath {

  /**
   * The property to determine the shortest path by.
   */
  private String property;

  private Edge[] edgeTo;

  private double[] distTo;

  private PriorityQueue<Edge> pq;

  /**
   * The ID number for the city to start with.
   */
  private int start;

  /**
   * The ID number for the city to end with.
   */
  private int end;

  /**
   * The graph to get data from.
   */
  private Graph map;


  /**
   * Constuctor
   *
   * @param map the graph to get data from
   * @param property the property to determine shortest path by
   */
  public DijkstraShortestPath(Graph map, int startIndex, int endIndex, String property) {
    this.map = map;
    this.property = property;
    this.start = startIndex;
    this.end = endIndex;
  }


  /**
   * Print the shortest path based on the previously determined property.
   */
  public void printShortestPath() {
    // Iterators
    int i, j, m;

    double[] values = new double[map.length + 1];

    // Cost of mappings
    double[][] LinkCost = new double[map.length + 1][map.length + 1];
    for (i = 1; i <= map.length; i++) {
      for (j = 1; j <= map.length; j++) {
        LinkCost[i][j] = map.getValueFor(i, j, this.property);
      }
    }

    // ID of the node travelled from
    int[] predNode = new int[map.length + 1];

    // Track which cities have been reached
    boolean[] Reached = new boolean[map.length + 1];
    for (i = 1; i <= map.length; i++) {
      Reached[i] = false;
    }
    Reached[this.start] = true;

    for (i = 1; i <= map.length; i++) {
      values[i] = LinkCost[this.start][i];
      if (LinkCost[this.start][i] < Double.POSITIVE_INFINITY) {
        predNode[i] = this.start;
      }
    }

    for (i = 1; i < map.length; i++) {
      for (j = 1; j <= map.length; j++) {
        if (!Reached[j])
          break;
      }

      for (m = j; m <= map.length; m++) {
        if (Reached[m] == false && values[m] < values[j]) {
          j = m;
        }
      }

      Reached[j] = true;

      for (m = 1; m <= map.length; m++) {
        if (Reached[m] == false) {
          if (values[j] + LinkCost[j][m] < values[m]) {
            values[m] = values[j] + LinkCost[j][m];
            predNode[m] = j;
          }
        }
      }
    }
    print(predNode);
  }

  private void print(int[] predNode) {
    int currentID = this.end;
    int lastID = 0;
    double collector = 0;
    StringBuilder flightpath = new StringBuilder();
    try {
      while (currentID != this.start) {
        if (currentID == 0) {
          throw new FlightNotFoundException();
        }
        lastID = currentID;
        flightpath.append(map.getCity(currentID).name + " to ");
        currentID = predNode[currentID];
        double value = map.getValueFor(lastID, currentID, property);
        collector += value;
        flightpath.append(map.getCity(currentID).name + " (");
        flightpath.append(value + ")\n");
      }
      System.out.println("Flight path (reverse order):");
      System.out.print(flightpath);
      System.out.println("Total: " + collector);
    } catch (FlightNotFoundException e) {
      System.out.println("Those cities are not connected!");
    }
  }


}

