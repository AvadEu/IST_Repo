public class RBNode {
    DictNode data;
    RBNode left, right, parent;
    boolean isRed;

    public RBNode(DictNode data) {
        this.data = data;
        this.isRed = true; // Nowe węzły zaczynają jako czerwone
    }
}
