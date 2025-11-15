import java.util.*;

public class RBTree {
    private RBNode root;
    private final RBNode NIL = new RBNode(null);

    public RBTree() {
        NIL.isRed = false;
        root = NIL;
    }

    public void insert(String word, int line) {
        DictNode entry = new DictNode(word);
        RBNode node = new RBNode(entry);
        node.left = NIL;
        node.right = NIL;

        RBNode y = null;
        RBNode x = root;

        while (x != NIL) {
            y = x;
            int cmp = word.compareTo(x.data.word);
            if (cmp == 0) {
                x.data.addLine(line);
                return;
            } else if (cmp < 0) {
                x = x.left;
            } else {
                x = x.right;
            }
        }

        node.parent = y;
        if (y == null) {
            root = node;
        } else if (word.compareTo(y.data.word) < 0) {
            y.left = node;
        } else {
            y.right = node;
        }

        node.data.addLine(line);
        fixInsert(node);
    }

    private void fixInsert(RBNode k) {
        while (k.parent != null && k.parent.isRed) {
            RBNode grandparent = k.parent.parent;
            if (k.parent == grandparent.left) {
                RBNode uncle = grandparent.right;
                if (uncle != null && uncle.isRed) {
                    k.parent.isRed = false;
                    uncle.isRed = false;
                    grandparent.isRed = true;
                    k = grandparent;
                } else {
                    if (k == k.parent.right) {
                        k = k.parent;
                        rotateLeft(k);
                    }
                    k.parent.isRed = false;
                    grandparent.isRed = true;
                    rotateRight(grandparent);
                }
            } else {
                RBNode uncle = grandparent.left;
                if (uncle != null && uncle.isRed) {
                    k.parent.isRed = false;
                    uncle.isRed = false;
                    grandparent.isRed = true;
                    k = grandparent;
                } else {
                    if (k == k.parent.left) {
                        k = k.parent;
                        rotateRight(k);
                    }
                    k.parent.isRed = false;
                    grandparent.isRed = true;
                    rotateLeft(grandparent);
                }
            }
        }
        root.isRed = false;
    }

    private void rotateLeft(RBNode x) {
        RBNode y = x.right;
        x.right = y.left;
        if (y.left != NIL) y.left.parent = x;
        y.parent = x.parent;
        if (x.parent == null) root = y;
        else if (x == x.parent.left) x.parent.left = y;
        else x.parent.right = y;
        y.left = x;
        x.parent = y;
    }

    private void rotateRight(RBNode x) {
        RBNode y = x.left;
        x.left = y.right;
        if (y.right != NIL) y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null) root = y;
        else if (x == x.parent.right) x.parent.right = y;
        else x.parent.left = y;
        y.right = x;
        x.parent = y;
    }

    public void inOrderPrint() {
        inOrderPrintRec(root);
    }

    private void inOrderPrintRec(RBNode node) {
        if (node == NIL || node == null) return;
        inOrderPrintRec(node.left);
        System.out.println(node.data);
        inOrderPrintRec(node.right);
    }

    public void bfsPrint() {
        Queue<RBNode> queue = new LinkedList<>();
        if (root != NIL) queue.add(root);

        while (!queue.isEmpty()) {
            RBNode current = queue.poll();
            System.out.println(current.data);

            if (current.left != NIL) queue.add(current.left);
            if (current.right != NIL) queue.add(current.right);
        }
    }

    public void delete(String word) {
        deleteNodeHelper(root, word);
    }

    private void deleteNodeHelper(RBNode node, String key) {
        RBNode z = NIL;
        RBNode x, y;
        while (node != NIL) {
            if (node.data.word.equals(key)) {
                z = node;
            }

            if (key.compareTo(node.data.word) < 0) {
                node = node.left;
            } else {
                node = node.right;
            }
        }

        if (z == NIL) {
            System.out.println("Nie znaleziono słowa: " + key);
            return;
        }

        y = z;
        boolean yOriginalColor = y.isRed;
        if (z.left == NIL) {
            x = z.right;
            rbTransplant(z, z.right);
        } else if (z.right == NIL) {
            x = z.left;
            rbTransplant(z, z.left);
        } else {
            y = minimum(z.right);
            yOriginalColor = y.isRed;
            x = y.right;
            if (y.parent == z) {
                x.parent = y;
            } else {
                rbTransplant(y, y.right);
                y.right = z.right;
                y.right.parent = y;
            }

            rbTransplant(z, y);
            y.left = z.left;
            y.left.parent = y;
            y.isRed = z.isRed;
        }

        if (!yOriginalColor) {
            fixDelete(x);
        }
    }

    private void rbTransplant(RBNode u, RBNode v) {
        if (u.parent == null) {
            root = v;
        } else if (u == u.parent.left) {
            u.parent.left = v;
        } else {
            u.parent.right = v;
        }
        v.parent = u.parent;
    }

    private RBNode minimum(RBNode node) {
        while (node.left != NIL) {
            node = node.left;
        }
        return node;
    }

    private void fixDelete(RBNode x) {
        RBNode s;
        while (x != root && !x.isRed) {
            if (x == x.parent.left) {
                s = x.parent.right;
                if (s.isRed) {
                    s.isRed = false;
                    x.parent.isRed = true;
                    rotateLeft(x.parent);
                    s = x.parent.right;
                }

                if (!s.left.isRed && !s.right.isRed) {
                    s.isRed = true;
                    x = x.parent;
                } else {
                    if (!s.right.isRed) {
                        s.left.isRed = false;
                        s.isRed = true;
                        rotateRight(s);
                        s = x.parent.right;
                    }

                    s.isRed = x.parent.isRed;
                    x.parent.isRed = false;
                    s.right.isRed = false;
                    rotateLeft(x.parent);
                    x = root;
                }
            } else {
                s = x.parent.left;
                if (s.isRed) {
                    s.isRed = false;
                    x.parent.isRed = true;
                    rotateRight(x.parent);
                    s = x.parent.left;
                }

                if (!s.left.isRed && !s.right.isRed) {
                    s.isRed = true;
                    x = x.parent;
                } else {
                    if (!s.left.isRed) {
                        s.right.isRed = false;
                        s.isRed = true;
                        rotateLeft(s);
                        s = x.parent.left;
                    }

                    s.isRed = x.parent.isRed;
                    x.parent.isRed = false;
                    s.left.isRed = false;
                    rotateRight(x.parent);
                    x = root;
                }
            }
        }
        x.isRed = false;
    }

}
