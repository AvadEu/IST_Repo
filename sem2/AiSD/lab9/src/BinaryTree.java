import java.util.*;

public class BinaryTree {

    public static class Node {
        String value;
        Node left, right;

        public Node(String value) {
            this.value = value;
        }

        public boolean isOperator() {
            return "+-*/%".contains(value);
        }
    }

    public Node buildTreeFromRPN(List<String> rpn) {
        Stack<Node> stack = new Stack<>();

        for (String token : rpn) {
            Node node = new Node(token);

            if (!node.isOperator()) {
                stack.push(node);
            } else {
                node.right = stack.pop();
                node.left = stack.pop();
                stack.push(node);
            }
        }

        return stack.pop();
    }

    public void printInorder(Node node) {
        if (node == null) return;

        if (node.isOperator()) {
            System.out.print("( ");
            printInorder(node.left);
            System.out.print(" " + node.value + " ");
            printInorder(node.right);
            System.out.print(" )");
        } else {
            System.out.print("( " + node.value + " )");
        }
    }

    public void printPostorder(Node node) {
        if (node == null) return;
        printPostorder(node.left);
        printPostorder(node.right);
        System.out.print(node.value + " ");
    }

    public int evaluate(Node node) {
        if (!node.isOperator()) {
            return Integer.parseInt(node.value);
        }

        int left = evaluate(node.left);
        int right = evaluate(node.right);

        int ret_value = 0;
        switch (node.value) {
            case "+": ret_value = left + right;
            break;
            case "-": ret_value = left - right;
            break;
            case "*": ret_value = left * right;
            break;
            case "/":
                if (right == 0) {
                    System.out.println("Błąd dzielenie przez 0!");
                    System.exit(0);
                } else {
                    ret_value = left / right;
                }
            break;
            case "%": ret_value = left % right;
            break;
        }
        return ret_value;
    }

    public int countLeaves(Node node) {
        if (node == null) return 0;
        if (node.left == null && node.right == null) return 1;
        return countLeaves(node.left) + countLeaves(node.right);
    }

    public int countNodes(Node node) {
        if (node == null) return 0;
        return 1 + countNodes(node.left) + countNodes(node.right);
    }

    public int treeHeight(Node node) {
        if (node == null) return 0;
        return 1 + Math.max(treeHeight(node.left), treeHeight(node.right));
    }

    public void printBreadthFirst(Node root) {
        if (root == null) return;

        Queue<Node> queue = new LinkedList<>();
        queue.add(root);

        while (!queue.isEmpty()) {
            Node current = queue.poll();
            System.out.print(current.value + " ");

            if (current.left != null) queue.add(current.left);
            if (current.right != null) queue.add(current.right);
        }
    }
}
