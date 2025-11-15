public class Main {
    public static void main(String[] args) {
        Graph graph = new Graph(5);

        graph.addEdge(0, 1, 10);
        graph.addEdge(0, 3, 30);
        graph.addEdge(0, 4, 100);
        graph.addEdge(1, 2, 50);
        graph.addEdge(2, 4, 10);
        graph.addEdge(3, 2, 20);
        graph.addEdge(3, 4, 60);

        int start = 4;

        graph.printAdjList();
        System.out.println();

        System.out.println("Dijkstra - najkrótsze ścieżki od miasta Wrocław:");
        Dijkstra.findShortestPaths(graph, start);

        System.out.println("\nPrzejście DFS:");
        DFS.dfs(graph, start);
    }
}
