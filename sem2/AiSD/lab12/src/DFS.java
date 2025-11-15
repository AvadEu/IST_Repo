import java.util.*;

public class DFS {
    public static void dfs(Graph graph, int start) {
        boolean[] visited = new boolean[graph.vertices];
        dfsRecursive(graph, start, visited);
    }

    private static void dfsRecursive(Graph graph, int vertex, boolean[] visited) {
        visited[vertex] = true;
        System.out.println("Odwiedzone miasto: " + vertex);

        for (Graph.Edge edge : graph.getNeighbors(vertex)) {
            if (!visited[edge.dest]) {
                dfsRecursive(graph, edge.dest, visited);
            }
        }
    }
}
