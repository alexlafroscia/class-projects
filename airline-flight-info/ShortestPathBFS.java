/**
 * Shortest Path BFS
 */

import java.util.*;

public class ShortestPathBFS {

  private Graph map;

  private int to;

  private int from;

  private int[] predNode;

  public ShortestPathBFS(Graph map, int to, int from) {
    this.map = map;
    this.to = to;
    this.from = from;

    predNode = new int[map.length + 1];
    Queue<Integer> pq = (Queue<Integer>)new LinkedList<Integer>();
    pq.add(to);
    predNode[to] = to;
    while (!(pq.size() == 0)) {
      int v = pq.poll();
      Iterator<Edge> neighbors = map.flightsFor(v).iterator();
      while (neighbors.hasNext()) {
        Edge edge = neighbors.next();
        if (predNode[edge.id] == 0) {
          pq.add(edge.id);
          predNode[edge.id] = v;
        }
      }
    }
  }

  public void print() {
    int currentID = this.from;
    StringBuilder str = new StringBuilder();
    try {
      while(currentID != this.to) {
        if (currentID == 0) {
          throw new FlightNotFoundException();
        }
        str.append(map.getCity(currentID).name);
        str.append(" --> ");
        currentID = predNode[currentID];
        str.append(map.getCity(currentID).name + "\n");
      }
      System.out.println("Flights (in reverse order):");
      System.out.print(str);
    } catch (FlightNotFoundException e) {
      System.out.println("Flight path not found.");
    }
  }
}

