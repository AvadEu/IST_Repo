public class Main {
    public static void main(String[] args) {
        Graph graph = new Graph();

        graph.addEdge("s", "a");
        graph.addEdge("s", "b");
        graph.addEdge("s", "c");
        graph.addEdge("a", "d");
        graph.addEdge("b", "d");
        graph.addEdge("b", "e");
        graph.addEdge("c", "f");
        graph.addEdge("d", "g");
        graph.addEdge("e", "g");
        graph.addEdge("e", "h");
        graph.addEdge("e", "i");
        graph.addEdge("g", "h");
        graph.addEdge("g", "i");
        graph.addEdge("h", "i");
        graph.addEdge("g", "t");
        graph.addEdge("h", "t");
        graph.addEdge("i", "t");

        System.out.println("BFS from 's': " + graph.bfs("s"));
        System.out.println("BFS from 'e': " + graph.bfs("e"));

        System.out.println("DFS from 's': " + graph.dfs("s"));
        System.out.println("DFS from 'e': " + graph.dfs("e"));
    }
}
