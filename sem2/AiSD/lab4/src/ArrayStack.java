public class ArrayStack<T> implements IStack<T> {
    private final T[] elements;
    private final int capacity;
    private int top;

    @SuppressWarnings("unchecked")
    public ArrayStack(int capacity) {
        this.capacity = capacity;
        elements = (T[]) new Object[capacity];
        top = -1;
    }

    public boolean isEmpty() {
        return top == -1;
    }

    public boolean isFull() {
        return top == capacity - 1;
    }

    public void push(T element) throws RuntimeException {
        if (isFull()) {
            throw new RuntimeException("Stos pełny!");
        }
        elements[++top] = element;
    }

    public T pop() throws RuntimeException {
        if (isEmpty()) {
            throw new RuntimeException("Stos pusty!");
        }
        T element = elements[top];
        elements[top--] = null;
        return element;
    }

    public T top() throws RuntimeException {
        if (isEmpty()) {
            throw new RuntimeException("Stos pusty!");
        }
        return elements[top];
    }

    public int size() {
        return top + 1;
    }

    public void odwroc() {
        if (isEmpty() || size() == 1) {
            return;
        }
        ArrayStack<T> t1 = new ArrayStack<>(capacity);

        while (!isEmpty()) {
            t1.push(pop());
        }

        ArrayStack<T> t2 = new ArrayStack<>(capacity);
        while (!t1.isEmpty()) {
            t2.push(t1.pop());
        }

        while (!t2.isEmpty()) {
            push(t2.pop());
        }
    }

    public String toString() {
        String output = "{";
        for (int i = 0; i < capacity; i++) {
            output += elements[i] + ", ";
        }
        output += "}";
        return output;
    }
}
