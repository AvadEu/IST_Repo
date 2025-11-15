package sinkingStack;

public class OptimalSinkingStack<T> {
    private Object[] elements;
    private int bottom;
    private int top;
    private int size;
    private final int capacity;

    public OptimalSinkingStack(int capacity) {
        this.capacity = capacity;
        this.elements = new Object[capacity];
        this.bottom = 0;
        this.top = -1;
        this.size = 0;
    }

    public void push(T element) {
        if (size == capacity) {
            bottom = (bottom + 1) % capacity;
            size--;
        }

        top = (top + 1) % capacity;
        elements[top] = element;
        size++;
    }

    public T pop() {
        if (isEmpty()) {
            throw new IllegalStateException("Stos jest pusty");
        }

        T element = (T) elements[top];
        elements[top] = null;
        top = (top - 1 + capacity) % capacity;
        size--;

        return element;
    }

    @SuppressWarnings("unchecked")
    public T peek() {
        if (isEmpty()) {
            throw new IllegalStateException("Stos jest pusty");
        }
        return (T) elements[top];
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public boolean isFull() {
        return size == capacity;
    }

    public int size() {
        return size;
    }

    public void printStack() {
        if (isEmpty()) {
            System.out.println("Stos jest pusty");
            return;
        }

        System.out.print("Stos (od dna do góry): ");
        int current = bottom;
        for (int i = 0; i < size; i++) {
            System.out.print(elements[current] + " ");
            current = (current + 1) % capacity;
        }
        System.out.println();
    }
}
