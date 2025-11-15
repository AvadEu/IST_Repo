import java.util.*;

public class Dijkstra {
    public static void findShortestPaths(Graph graph, int start) {
        int[] distances = new int[graph.vertices];
        Arrays.fill(distances, Integer.MAX_VALUE);
        distances[start] = 0;

        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        pq.offer(new int[]{start, 0});

        while (!pq.isEmpty()) {
            int[] current = pq.poll();
            int currentNode = current[0];
            int currentDist = current[1];

            for (Graph.Edge edge : graph.getNeighbors(currentNode)) {
                int newDist = currentDist + edge.weight;
                if (newDist < distances[edge.dest]) {
                    distances[edge.dest] = newDist;
                    pq.offer(new int[]{edge.dest, newDist});
                }
            }
        }

        for (int i = 0; i < distances.length; i++) {
            if (distances[i] != Integer.MAX_VALUE) {
                System.out.println("Miasto " + i + " (dystans: " + distances[i] + ")");
            }
        }
    }
}
