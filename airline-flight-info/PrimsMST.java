/**
 * MST Implemented using Lazy Prim's Algorithm.
 */

import java.util.*;

public class PrimsMST {

  private boolean[] marked;

  /**
   * Queue to hold the minimum spanning tree.
   * Actually will be backed by a LinkedList, which implements the Queue
   * interface.
   */
  private Queue<Edge> mst;

  private PriorityQueue<Edge> pq;

  private Graph map;

  private int numFound;

  public PrimsMST(Graph map) {
    this.map = map;
    pq = new PriorityQueue<Edge>();
    marked = new boolean[map.length + 1];
    mst = (Queue<Edge>) new LinkedList<Edge>();
    numFound = 0;

    // Visit the first city
    this.visit(map, 1);

    while (numFound != map.length) {
      PrintService.printFlightTableHeader("Minimum Spanning Tree");
      while (!(pq.size() == 0)) {
        Edge e = pq.poll();
        int v = e.originator;
        int w = e.id;
        if (marked[v] && marked[w]) continue;
        PrintService.printFlightTableRow(map, e.originator, e);
        if (!marked[v]) visit(map, v);
        if (!marked[w]) visit(map, w);
      }
      System.out.println();

      for (int i = 1; i < map.length + 1; i++) {
        if (!marked[i]) {
          marked[i] = true;
          visit(map, i);
          break;
        }
      }
    }
  }


  /**
   * Marks a vertex (city) as visited.
   * Also adds all connecting cities to the priority queue
   */
  private void visit(Graph map, int index) {
    marked[index] = true;
    numFound++;
    for (Edge e : map.flightsFor(index)) {
      if (!marked[e.id]) {
        pq.add(e);
      }
    }
  }

}
