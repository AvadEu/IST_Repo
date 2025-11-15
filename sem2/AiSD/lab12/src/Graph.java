import java.util.*;

public class Graph {
    final String[] cities = {"Wrocław", "Oława", "Brzeg", "Nysa", "Opole"};
    int vertices;
    List<List<Edge>> adjList;

    public Graph(int vertices) {
        this.vertices = vertices;
        adjList = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }

    public void addEdge(int src, int dest, int weight) {
        adjList.get(src).add(new Edge(dest, weight));
    }

    public List<Edge> getNeighbors(int vertex) {
        return adjList.get(vertex);
    }

    public static class Edge {
        int dest;
        int weight;

        public Edge(int dest, int weight) {
            this.dest = dest;
            this.weight = weight;
        }
    }

    public void printAdjList() {
        System.out.println("Lista sąsiedztwa:");
        for (int i = 0; i < adjList.size(); i++) {
            System.out.print("Miasto " + i + " (" + cities[i] + ") -> ");
            for (Edge edge : adjList.get(i)) {
                System.out.print("(" + edge.dest + ", " + edge.weight + ") ");
            }
            System.out.println();
        }
    }
}
