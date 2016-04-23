/**
 * Airline.
 * CS 1501
 * Project 3
 * Mar 17, 2015
 *
 * @author Alex LaFroscia
 */

import java.util.*;
import java.io.*;
import java.math.BigDecimal;

public class Airline {

  /**
   * The main method to be executed.
   */
  public static void main(String[] args) {

    String fileName = getFileName();

    Graph map = createGraphFromFile(fileName);

    while (true) {
      int selection = getMenuSelection();

      switch(selection) {
        case 1:
          PrintService.printFlightList(map, "Flight List");
          break;
        case 2:
          minimumSpanningTree(map);
          break;
        case 3:
          shortestFlight(map, "distance");
          break;
        case 4:
          shortestFlight(map, "price");
          break;
        case 5:
          shortestFightByJumps(map);
          break;
        case 6:
          cheaperThan(map);
          break;
        case 7:
          addFlight(map);
          break;
        case 8:
          removeFlight(map);
          break;
        case 0:
          saveAndExit(map, fileName);
          break;
        default:
          System.out.println("Please choose a valid option.");
          break;
      }
    }

  }


  /**
   * Get the name of the file to open from the user.
   * Asks the user what file they want to open, and returns a string of the file
   * name.
   *
   * @return the name of the file to open
   */
  private static String getFileName() {
    System.out.println("Which file would you like to open?");
    System.out.print("> ");
    Scanner a = new Scanner(System.in);
    return a.nextLine();
  }


  /**
   * Creates a map of cities, given the name of the file to open.
   * Using the given file name, this method reads in the contents of the file
   * and creates a map (graph) of the cities.  This graph is represented as an
   * adjacency list.
   *
   * If the file is not found, the stack will be printed out and the program
   * will exit.
   *
   * The object returned is a Graph object that contains both the adjacency list
   * that maps the neighbors of each city, but also hash maps that can be used
   * to efficiently look up a city by either the name or ID.
   *
   * @param  filename    the name of the file to open
   * @return             the map of the cities
   */
  private static Graph createGraphFromFile(String fileName) {
    Graph map = null;
    try {
      BufferedReader br = new BufferedReader(new FileReader(fileName));
      int numberOfCities = Integer.parseInt(br.readLine());
      map = new Graph(numberOfCities);

      // For each city in the file,
      for (int i = 1; i <= numberOfCities; i++) {
        String name = br.readLine();
        City city = new City(i, name);
        map.addCity(city);
      }

      String line;
      while ((line = br.readLine()) != null) {
        String[] split = line.split("\\s+");

        map.add(Integer.parseInt(split[0]), Integer.parseInt(split[1]),
                Integer.parseInt(split[2]), new BigDecimal(split[3]));
      }

    } catch(IOException e){
      e.printStackTrace();
      System.exit(1);
    }

    return map;
  }


  /**
   * Display the menu of actions to choose from.
   */
  public static int getMenuSelection() {
    Scanner input = new Scanner(System.in);
    System.out.println("\nWhat would you like to do?");
    System.out.println("  1. Print list of flights");
    System.out.println("  2. Print minimum spanning tree");
    System.out.println("  3. Get shortest path by distance");
    System.out.println("  4. Get shortest path by price");
    System.out.println("  5. Get shortest path by number of jumps");
    System.out.println("  6. Find flight cheaper than...");
    System.out.println("  7. Add a flight to the list");
    System.out.println("  8. Remove a flight from the list");
    System.out.println("  0. Save and exit the program");
    System.out.print("\n> ");
    try {
      return input.nextInt();
    } catch (InputMismatchException e) {
      return 10;
    }
  }


  public static void shortestFlight(Graph map, String property) {
    System.out.println("City list:");
    PrintService.printCityList(map);
    System.out.println("Pick the cities to search between");
    Scanner input = new Scanner(System.in);
    System.out.print("\nFirst city > ");
    int choice = input.nextInt();

    System.out.print("Second city > ");
    int choice2 = input.nextInt();
    System.out.println();
    Scanner scanner = new Scanner(System.in);

    if (property.equals("distance")) {
      map.shortestFlightsByDistance(choice, choice2);
    } else if (property.equals("price")) {
      map.shortestFlightsByPrice(choice, choice2);
    }
  }


  /**
   * Map the shortest path between cities by number of jumps.
   * Uses BFS.
   *
   * @param map graph to search by
   */
  public static void shortestFightByJumps(Graph map) {
    System.out.println("City list:");
    PrintService.printCityList(map);
    System.out.println("Pick the cities to search between");
    Scanner input = new Scanner(System.in);
    System.out.print("\nFirst city > ");
    int choice = input.nextInt();

    System.out.print("Second city > ");
    int choice2 = input.nextInt();
    System.out.println();
    Scanner scanner = new Scanner(System.in);

    ShortestPathBFS bfs = new ShortestPathBFS(map, choice, choice2);
    bfs.print();
  }


  /**
   * Print the minimum spanning tree for the route database.
   *
   * @param map the graph to search
   */
  public static void minimumSpanningTree(Graph map) {
    PrimsMST mst = new PrimsMST(map);
  }


  /**
   * Add a new flight to the map.
   *
   * @param map the map object to add to
   */
  public static void addFlight(Graph map) {
    // Get the origin city
    System.out.println("What is the origin city?");
    map.printCityList();
    Scanner input = new Scanner(System.in);
    System.out.print("\n> ");
    int originID = input.nextInt();

    // Get the destination city
    System.out.println("What is the destination city?");
    map.printCityList();
    input = new Scanner(System.in);
    System.out.print("\n> ");
    int destinationID = input.nextInt();

    // Get the distance
    System.out.println("What is the distance between the two cities?");
    input = new Scanner(System.in);
    System.out.print("\n> ");
    int distance = input.nextInt();

    // Get the price
    System.out.println("What is the price to fly between these cities?");
    input = new Scanner(System.in);
    System.out.print("\n> ");
    BigDecimal price = input.nextBigDecimal();

    // Add the edge to the graph
    map.add(originID, destinationID, distance, price);
    System.out.println("Your flight as been added!");
  }


  /**
   * Remove a flight from the map.
   *
   * @param map the map to remove a flight from.
   */
  public static void removeFlight(Graph map) {
    PrintService.printFlightList(map, "Flight List");
    System.out.println();
    PrintService.printCityList(map);
    System.out.println("Pick the cities for the route you want to remove");
    Scanner input = new Scanner(System.in);
    System.out.print("\nFirst city > ");
    int choice = input.nextInt();

    System.out.print("Second city > ");
    int choice2 = input.nextInt();
    System.out.println();

    // Remove the flight
    try {
      map.removeFlight(choice, choice2);
      System.out.printf("Route was removed.\n", choice);
    } catch (FlightNotFoundException e) {
      System.out.println("Those cities do not match a route in our system.");
    }

  }


  /**
   * Find a flight cheaper than some price.
   *
   * @param map the map to search for
   */
  public static void cheaperThan(Graph map) {
    // Get the price
    System.out.println("What's the maxiumum price to search for?");
    System.out.print("> ");
    Scanner input = new Scanner(System.in);
    BigDecimal price = input.nextBigDecimal();

    PriceSearch priceSearch = new PriceSearch(map, price);
    for (String list : priceSearch.routes) {
      System.out.println(list);
    }
  }


  /**
   * Save and Exit
   *
   * @param map the graph to save data from
   * @param filename the name of the file to save the graph data to
   */
  public static void saveAndExit(Graph map, String fileName) {
    try {
      PrintWriter writer = new PrintWriter(fileName, "UTF-8");
      map.save(writer);
      writer.close();
    } catch (Exception e) {
      e.printStackTrace();
      System.exit(1);
    }
    System.out.println("File saved successfully. Have a nice day!");
    System.exit(0);
  }

}

