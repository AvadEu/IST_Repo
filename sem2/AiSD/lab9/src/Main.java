import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Podaj wyrażenie: ");
        String expression = sc.nextLine();

        List<String> rpn = ONPConverter.toONP(expression);

        BinaryTree tree = new BinaryTree();
        BinaryTree.Node root = tree.buildTreeFromRPN(rpn);

        int value = tree.evaluate(root);

        System.out.print("Wyniki:\n1. wyrażenie z nawiasami (metoda inorder): ");
        tree.printInorder(root);
        System.out.println(" = " + value);

        System.out.print("2. wyrażenie w postaci ONP (metoda postorder): ");
        tree.printPostorder(root);
        System.out.println(" = " + value);

        System.out.println("Liczba liści: " + tree.countLeaves(root));
        System.out.println("Liczba węzłów: " + tree.countNodes(root));
        System.out.println("Wysokość drzewa: " + tree.treeHeight(root));

        System.out.println("Przejście przez drzewo wszerz: ");
        tree.printBreadthFirst(root);
    }
}
