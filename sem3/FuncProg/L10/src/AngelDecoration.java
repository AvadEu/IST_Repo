import java.util.List;

class AngelDecoration implements IDecoration {
    @Override
    public void decorate(List<StringBuilder> treeRepresentation) {
        if (treeRepresentation.isEmpty()) return;

        StringBuilder topRow = treeRepresentation.get(0);
        int midIndex = topRow.indexOf("*");

        if (midIndex != -1) {
            topRow.setCharAt(midIndex, 'A');
        }
    }
    @Override
    public String toString() { return "Angel (A)"; }
}