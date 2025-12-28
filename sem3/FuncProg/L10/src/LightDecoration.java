import java.util.List;

class LightDecoration implements IDecoration {
    @Override
    public void decorate(List<StringBuilder> treeRepresentation) {
        int starCounter = 0;
        for (StringBuilder line : treeRepresentation) {
            for (int i = 0; i < line.length(); i++) {
                if (line.charAt(i) == '*') {
                    starCounter++;
                    if (starCounter % 3 == 0) {
                        line.setCharAt(i, 'x');
                    }
                }
            }
        }
    }
    @Override
    public String toString() { return "Lights (x)"; }
}