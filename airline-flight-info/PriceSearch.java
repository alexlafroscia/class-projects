import java.util.*;
import java.math.BigDecimal;

public class PriceSearch {

  private boolean[] visited;

  private BigDecimal price;

  public ArrayList<String> routes;

  public PriceSearch(Graph map, BigDecimal price) {
    this.visited = new boolean[map.length + 1];
    this.routes = new ArrayList<String>();
    this.price = price;
    for (int i = 1; i <= map.length; i++) {
      String cityName = map.getCity(i).name;
      visit(map, i, cityName, new BigDecimal(0));
    }
  }

  private void visit(Graph map, int city, String cityList, BigDecimal price) {
    // Base case: city already visited
    if (visited[city]) {
      return;
    }

    // Base case: cost exceeded
    if (price.compareTo(this.price) > 0) {
      return;
    }

    if (price.compareTo(new BigDecimal(0)) > 0) {
      routes.add(cityList + " (" + price.toString() + ")");
    }

    // Mark it as visited
    visited[city] = true;
    Iterator<Edge> neighbors = map.flightsFor(city).iterator();
    while(neighbors.hasNext()) {
      Edge neighbor = neighbors.next();
      visit(map, neighbor.id,
            cityList + " --> " + map.getCity(neighbor.id).name,
            price.add(neighbor.price));
    }
    // Un-visit before returning
    visited[city] = false;
  }
}

