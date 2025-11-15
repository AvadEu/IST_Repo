import java.io.Serializable;
import java.util.Comparator;

public class L2KCzS<E> implements Serializable {
    private final Node<E> sentinel;
    private int size;

    private static class Node<E> implements Serializable {
        E data;
        Node<E> next;
        Node<E> prev;

        Node(E data) {
            this.data = data;
        }

        Node() {
            this.data = null;
        }
    }

    public L2KCzS() {
        sentinel = new Node<>();

        sentinel.next = sentinel;
        sentinel.prev = sentinel;

        size = 0;
    }

    public boolean isEmpty() {
        return sentinel.next == sentinel;
    }

    public int size() {
        return size;
    }

    public void add(E element) {
        Node<E> newNode = new Node<>(element);

        newNode.prev = sentinel.prev;
        newNode.next = sentinel;

        sentinel.prev.next = newNode;
        sentinel.prev = newNode;

        size++;
    }

    public void add(int index, E element) {
        if (index < 0 || index > size) {
            throw new IndexOutOfBoundsException();
        }

        Node<E> current = sentinel;
        for (int i = 0; i <= index; i++) {
            current = current.next;
        }

        Node<E> newNode = new Node<>(element);
        newNode.next = current;
        newNode.prev = current.prev;

        current.prev.next = newNode;
        current.prev = newNode;

        size++;
    }

    public void addSorted(E element, Comparator<E> comparator) {

        if (element == null) {
            throw new NullPointerException("Nie można dodać null do listy");
        }

        if (isEmpty()) {
            add(element);
            return;
        }

        Node<E> current = sentinel.next;
        while (current != sentinel && comparator.compare(current.data, element) < 0) {
            current = current.next;
        }

        Node<E> newNode = new Node<>(element);
        newNode.next = current;
        newNode.prev = current.prev;

        current.prev.next = newNode;
        current.prev = newNode;

        size++;
    }

    public boolean remove(E element) {
        if (isEmpty()) {
            return false;
        }

        Node<E> current = sentinel.next;
        while (current != sentinel) {
            if ((current.data == null && element == null) ||
                    (current.data != null && current.data.equals(element))) {

                current.prev.next = current.next;
                current.next.prev = current.prev;

                size--;
                return true;
            }
            current = current.next;
        }

        return false;
    }


    public E get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }

        Node<E> current = sentinel.next;
        for (int i = 0; i < index; i++) {
            current = current.next;
        }

        return current.data;
    }
}
