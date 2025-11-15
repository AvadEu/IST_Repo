import java.util.*;

public class Node implements Comparable<Node> {
    private final String value;
    private final List<Node> neighbors;

    public Node(String value) {
        this.value = value;
        this.neighbors = new ArrayList<>();
    }

    public String getValue() {
        return value;
    }

    public List<Node> getNeighbors() {
        return neighbors;
    }

    public void addNeighbor(Node neighbor) {
        neighbors.add(neighbor);
    }

    @Override
    public int compareTo(Node other) {
        return this.value.compareTo(other.value);
    }

    @Override
    public String toString() {
        return value;
    }
}
