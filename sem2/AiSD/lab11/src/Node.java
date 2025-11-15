import java.util.Objects;

class Node implements Comparable<Node> {
    char ch;
    int freq;
    Node left, right;

    // Konstruktor dla liścia
    public Node(char ch, int freq) {
        this.ch = ch;
        this.freq = freq;
    }

    // Konstruktor dla węzła wewnętrznego
    public Node(Node left, Node right) {
        this.ch = '\0'; // znak specjalny dla węzłów wewnętrznych
        this.freq = left.freq + right.freq;
        this.left = left;
        this.right = right;
    }

    public boolean isLeaf() {
        return left == null && right == null;
    }

    @Override
    public int compareTo(Node other) {
        return this.freq - other.freq;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Node)) return false;
        Node node = (Node) o;
        return ch == node.ch && freq == node.freq &&
                Objects.equals(left, node.left) &&
                Objects.equals(right, node.right);
    }

    @Override
    public int hashCode() {
        return Objects.hash(ch, freq, left, right);
    }
}
