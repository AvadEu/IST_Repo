import java.util.List;

class BaubleDecoration implements IDecoration {
    @Override
    public void decorate(List<StringBuilder> treeRepresentation) {
        int starCounter = 0;
        for (StringBuilder line : treeRepresentation) {
            for (int i = 0; i < line.length(); i++) {
                if (line.charAt(i) == '*') {
                    starCounter++;
                    if (starCounter % 2 == 0) {
                        line.setCharAt(i, 'o');
                    }
                }
            }
        }
    }
    @Override
    public String toString() { return "Baubles (o)"; }
}