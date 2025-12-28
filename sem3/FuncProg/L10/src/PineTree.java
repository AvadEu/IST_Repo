public class PineTree extends ChristmasTree {

    public PineTree(int height) {
        super(height);
        generateTree();
    }

    @Override
    protected void generateTree() {
        // Dla każdego poziomu i: liczba spacji = height - 1 - i, liczba gwiazdek = 2*i + 1
        for (int i = 0; i < height; i++) {
            StringBuilder line = new StringBuilder();

            // Spacje
            for (int s = 0; s < height - 1 - i; s++) {
                line.append(" ");
            }

            // Gwiazdki
            for (int stars = 0; stars < (2 * i + 1); stars++) {
                line.append("*");
            }

            treeRepresentation.add(line);
        }

        // Pieniek
        StringBuilder trunk = new StringBuilder();
        for (int s = 0; s < height - 1; s++) trunk.append(" ");
        trunk.append("#");
        treeRepresentation.add(trunk);
    }
}