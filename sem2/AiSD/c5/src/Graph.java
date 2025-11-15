import java.util.*;

public class Graph {
    private Map<String, Node> nodes = new HashMap<>();

    public Node getOrCreateNode(String value) {
        return nodes.computeIfAbsent(value, Node::new);
    }

    public void addEdge(String from, String to) {
        Node fromNode = getOrCreateNode(from);
        Node toNode = getOrCreateNode(to);
        fromNode.addNeighbor(toNode);
        toNode.addNeighbor(fromNode);
    }

    public List<String> bfs(String startValue) {
        Set<String> visited = new HashSet<>();
        Queue<Node> queue = new LinkedList<>();
        List<String> order = new ArrayList<>();

        Node start = nodes.get(startValue);
        if (start == null) return order;

        visited.add(start.getValue());
        queue.add(start);

        while (!queue.isEmpty()) {
            Node current = queue.poll();
            order.add(current.getValue());

            List<Node> sortedNeighbors = new ArrayList<>(current.getNeighbors());
            Collections.sort(sortedNeighbors);
            for (Node neighbor : sortedNeighbors) {
                if (!visited.contains(neighbor.getValue())) {
                    visited.add(neighbor.getValue());
                    queue.add(neighbor);
                }
            }
        }
        return order;
    }

    public List<String> dfs(String startValue) {
        Set<String> visited = new HashSet<>();
        List<String> order = new ArrayList<>();
        Node start = nodes.get(startValue);
        if (start == null) return order;
        dfsRecursive(start, visited, order);
        return order;
    }

    private void dfsRecursive(Node current, Set<String> visited, List<String> order) {
        visited.add(current.getValue());
        order.add(current.getValue());

        List<Node> sortedNeighbors = new ArrayList<>(current.getNeighbors());
        Collections.sort(sortedNeighbors);
        for (Node neighbor : sortedNeighbors) {
            if (!visited.contains(neighbor.getValue())) {
                dfsRecursive(neighbor, visited, order);
            }
        }
    }
}
