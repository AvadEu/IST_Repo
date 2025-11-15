import java.util.ArrayList;

public class DictNode implements Comparable<DictNode> {
    String word;
    ArrayList<Integer> lines;

    public DictNode(String word) {
        this.word = word;
        this.lines = new ArrayList<>();
    }

    public void addLine(int lineNumber) {
        lines.add(lineNumber);
    }

    @Override
    public int compareTo(DictNode other) {
        return this.word.compareTo(other.word);
    }

    @Override
    public String toString() {
        return word + " - " + lines.toString().replaceAll("[\\[\\]]", "");
    }
}
