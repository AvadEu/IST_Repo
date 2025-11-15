import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;

public class Huffman {

    private Node root;
    private Map<Character, String> codes = new HashMap<>();

    public void buildTree(String text) {
        int[] freq = new int[256];
        for (char c : text.toCharArray()) {
            freq[c]++;
        }

        PriorityQueue<Node> pq = new PriorityQueue<>();
        for (char c = 0; c < freq.length; c++) {
            if (freq[c] > 0) {
                pq.add(new Node(c, freq[c]));
            }
        }

        while (pq.size() > 1) {
            Node left = pq.poll();
            Node right = pq.poll();
            Node parent = new Node(left, right);
            pq.add(parent);
        }

        root = pq.poll();

        buildCodes(root, "");
    }

    private void buildCodes(Node node, String code) {
        if (node == null) return;

        if (node.isLeaf()) {
            codes.put(node.ch, code.length() > 0 ? code : "0");
        } else {
            buildCodes(node.left, code + '0');
            buildCodes(node.right, code + '1');
        }
    }

    public String encode(String text) {
        StringBuilder sb = new StringBuilder();
        for (char c : text.toCharArray()) {
            sb.append(codes.get(c));
        }
        return sb.toString();
    }

    public String decode(String encoded) {
        StringBuilder sb = new StringBuilder();
        Node current = root;
        for (char bit : encoded.toCharArray()) {
            current = (bit == '0') ? current.left : current.right;

            if (current.isLeaf()) {
                sb.append(current.ch);
                current = root;
            }
        }
        return sb.toString();
    }

    public Map<Character, String> getCodes() {
        return codes;
    }
}
