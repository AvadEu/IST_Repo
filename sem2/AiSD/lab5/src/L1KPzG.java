public class L1KPzG<E> {
    private Node<E> head;
    private int size;

    private static class Node<E> {
        E data;
        Node<E> next;

        Node(E data) {
            this.data = data;
            this.next = null;
        }
    }

    public L1KPzG() {
        head = null;
        size = 0;
    }

    public void add(E element) {
        Node<E> newNode = new Node<>(element);
        newNode.next = head;
        head = newNode;
        size++;
    }

    public E removeFirst() {
        if (isEmpty()) {
            return null;
        }

        E data = head.data;
        head = head.next;
        size--;
        return data;
    }

    public E getFirst() {
        if (isEmpty()) {
            return null;
        }

        return head.data;
    }

    public boolean isEmpty() {
        return head == null;
    }

    public int size() {
        return size;
    }
}
