import java.io.*;
import java.util.*;
import java.math.BigDecimal;

/**
 * Graph of cities, as an adjacency list.
 */
public class Graph {

  /**
   * Map of names to city objects.
   * Can be used to look up a city based on the name.
   */
  private HashMap<String, City> citiesByName = new HashMap<>();


  /**
   * Map of ids to city objects.
   * Can be used to look up a city based on the id.
   */
  private HashMap<Integer, City> citiesByID = new HashMap<>();


  /**
   * Array to hold a city's neighbors.
   */
  private LinkedList<Edge>[] adjacencyList;


  /**
   * The number of items in the adjacency list.
   */
  public int length;


  /**
   * Constructor
   */
  public Graph(int size) {
    this.adjacencyList = new LinkedList[size + 1];
    this.length = size;
    for (int i = 0; i < size; i++) {
      this.adjacencyList[i] = new LinkedList<Edge>();
    }
  }


  /**
   * Add a new connection between cities to the map.
   *
   * @param index    The ID number of the "to" city
   * @param from     The city that is being travelled to
   * @param distance The distance between the two cities
   * @param price    The price to travel between two cities
   *
   */
  public void add(int from, int to, int distance, BigDecimal price) {
    Edge edge1 = new Edge(to, from, distance, price);
    this.adjacencyList[from - 1].addLast(edge1);

    Edge edge2 = new Edge(from, to, distance, price);
    this.adjacencyList[to - 1].addLast(edge2);
  }


  /*
   * Remove a flight based on the flight number
   */
  public void removeFlight(int in1, int in2) throws FlightNotFoundException {
    // Set up counters
    int counter = 0;
    boolean found = false;

    Iterator<Edge> neighbors = this.flightsFor(in1).iterator();
    while (neighbors.hasNext() && !found) {
      counter++;
      Edge neighbor = neighbors.next();
      if (neighbor.id == in2) {
        neighbors.remove();
        found = true;
      }
    }

    if (!found) {
      throw new FlightNotFoundException("Route not found");
    }

    // Reset counters
    counter = 0;
    found = false;

    neighbors = this.flightsFor(in2).iterator();
    while (neighbors.hasNext() && !found) {
      counter++;
      Edge neighbor = neighbors.next();
      if (neighbor.id == in1) {
        neighbors.remove();
        found = true;
      }
    }

  }


  /**
   * Get the flights for a city based on the name.
   *
   * @param name the name of the city
   * @return     the first neighbor of the city, or null if none exist
   */
  public LinkedList<Edge> flightsFor(String name) {
    int id = this.citiesByName.get(name).id;
    return this.flightsFor(id);
  }


  /**
   * Get this flights for a city based on the ID.
   *
   * @param id the ID number for the city
   * @return   the first neighbor of the city, or null if none exist
   */
  public LinkedList<Edge> flightsFor(int id) {
    return this.adjacencyList[id - 1];
  }


  /**
   * Get a city based on the ID number.
   *
   * @param id the city's ID number
   * @return   the city object
   */
  public City getCity(int id) {
    return this.citiesByID.get(id);
  }


  /**
   * Get a city based on the name.
   *
   * @param name the name of the city
   * @return     the city object
   */
  public City getCity(String name) {
    return this.citiesByName.get(name);
  }


  /**
   * Add a city to the hash maps.
   *
   * @param City the city to add
   */
  public void addCity(City city) {
    this.citiesByID.put(city.id, city);
    this.citiesByName.put(city.name, city);
  }


  /**
   * Print a list of all of the cities, along with their corresponding ID
   * numbers.
   */
  public void printCityList() {
    for (int i = 1; i <= this.length; i++) {
      City city = this.getCity(i);
      System.out.printf("%3d. %s\n", city.id, city.name);
    }
  }


  public double getValueFor(int to, int from, String property) {
    LinkedList<Edge> flights = this.flightsFor(to);
    Iterator<Edge> iterator = flights.iterator();
    boolean found = false;
    Edge edge = null;
    while(!found && iterator.hasNext()) {
      edge = iterator.next();
      if (edge.id == from) {
        found = true;
      }
    }

    // Return either the distance or price of the edge,
    // or infinity if the edge wasn't found.
    double toReturn = Double.POSITIVE_INFINITY;
    if (found && property.equals("distance")) {
      toReturn = edge.distance;
    }
    if (found && property.equals("price")) {
      toReturn = edge.price.doubleValue();
    }
    return toReturn;
  }


  public void shortestFlightsByDistance(int start, int end) {
    DijkstraShortestPath d = new DijkstraShortestPath(this, start, end, "distance");
    d.printShortestPath();
  }


  public void shortestFlightsByPrice(int start, int end) {
    DijkstraShortestPath d = new DijkstraShortestPath(this, start, end, "price");
    d.printShortestPath();
  }


  /**
   * Write all of the needed data to the file.
   */
  public void save(PrintWriter writer) {
    int[][] printedList = new int[this.length + 1][this.length + 1];
    writer.println(this.length);
    for (int i = 1; i <= this.length; i++) {
      City city = this.getCity(i);
      writer.println(city.name);
    }
    for (int i = 1; i <= this.length; i++) {
      Iterator<Edge> neighbors = this.flightsFor(i).iterator();
      while (neighbors.hasNext()) {
        Edge e = neighbors.next();
        if (printedList[i][e.id] == 0) {
          printedList[i][e.id] = 1;
          printedList[e.id][i] = 1;
          writer.println(i + " " + e.id + " " + e.distance + " " + e.price.setScale(2));
        }
      }
    }
  }

}

