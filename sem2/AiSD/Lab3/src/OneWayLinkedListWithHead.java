import java.util.*;

public class OneWayLinkedListWithHead<E extends Comparable<E>> extends AbstractSequentialList<E> {
    private Node<E> head;
    private int size;

    public OneWayLinkedListWithHead() {
        head = new Node<>(null);
        size = 0;
    }

    private static class Node<E> {
        E data;
        Node<E> next;

        Node(E data) {
            this.data = data;
            this.next = null;
        }
    }

    @Override
    public int size() {
        return size;
    }

    @Override
    public ListIterator<E> listIterator(int index) {
        if (index < 0 || index > size) {
            throw new IndexOutOfBoundsException("Index: " + index);
        }
        return new LinkedListIterator(index);
    }

    private class LinkedListIterator implements ListIterator<E> {
        private Node<E> current;
        private Node<E> previous;
        private int currentIndex;
        private boolean canRemove;

        LinkedListIterator(int index) {
            current = head.next;
            previous = head;
            currentIndex = 0;

            while (currentIndex < index && current != null) {
                previous = current;
                current = current.next;
                currentIndex++;
            }
        }

        @Override
        public boolean hasNext() {
            return current != null;
        }

        @Override
        public E next() {
            if (!hasNext()) {
                throw new NoSuchElementException();
            }
            E data = current.data;
            previous = current;
            current = current.next;
            currentIndex++;
            return data;
        }

        @Override
        public boolean hasPrevious() {
            return previous != head;
        }

        @Override
        public E previous() {
            if (!hasPrevious()) {
                throw new NoSuchElementException();
            }
            E data = previous.data;
            current = previous;
            previous = findPrevious(previous);
            currentIndex--;
            return data;
        }

        private Node<E> findPrevious(Node<E> node) {
            Node<E> temp = head;
            while (temp.next != node && temp.next != null) {
                temp = temp.next;
            }
            return temp;
        }

        @Override
        public int nextIndex() {
            return currentIndex;
        }

        @Override
        public int previousIndex() {
            return currentIndex - 1;
        }

        public void remove() {
            if (previous == head || current == null) {
                throw new IllegalStateException("Cannot remove element.");
            }

            previous.next = current.next;
            if (current == previous) {
                current = null;
            } else {
                current = previous.next;
            }

            size--;
        }

        @Override
        public void set(E e) {
            if (current == null) {
                throw new IllegalStateException("Cannot set element.");
            }
            current.data = e;
        }

        @Override
        public void add(E e) {
            Node<E> newNode = new Node<>(e);

            if (previous == head) {
                newNode.next = head.next;
                head.next = newNode;
            } else {
                newNode.next = previous.next;
                previous.next = newNode;
                previous = newNode;
            }

            size++;
        }
    }

    public void addSorted(E element) {
        ListIterator<E> iterator = listIterator(0);

        while (iterator.hasNext()) {
            if (iterator.next().compareTo(element) > 0) {
                iterator.previous();
                break;
            }
        }

        iterator.add(element);
    }

    public void addToEnd(E element) {
        addSorted(element);
    }

    @Override
    public String toString() {
        String oputput = "";
        ListIterator<E> iterator = listIterator(0);

        while (iterator.hasNext()) {
            oputput += iterator.next() + "\n";
        }
        return oputput;
    }

    public void removeHiddenCards() {
        Node<E> current = head;

        while (current.next != null) {
            if (current.next.data instanceof Karta && !((Karta) current.next.data).isOdkryta()) {
                current.next = current.next.next;
                size--;
            } else {
                current = current.next;
            }
        }
    }

}
