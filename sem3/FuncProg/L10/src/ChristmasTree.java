import java.util.ArrayList;
import java.util.List;

public abstract class ChristmasTree {
    protected List<StringBuilder> treeRepresentation;
    protected int height;

    public ChristmasTree(int height) {
        if (height < 2) throw new IllegalArgumentException("Wysokość musi być >= 2");
        this.height = height;
        this.treeRepresentation = new ArrayList<>();
    }

    protected abstract void generateTree();

    public void applyDecoration(IDecoration decoration) {
        if (decoration != null) {
            decoration.decorate(this.treeRepresentation);
        }
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (StringBuilder line : treeRepresentation) {
            sb.append(line).append("\n");
        }
        return sb.toString();
    }

    public List<StringBuilder> getRepresentation() {
        return treeRepresentation;
    }
}