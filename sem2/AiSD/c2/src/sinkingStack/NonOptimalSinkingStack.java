package sinkingStack;

import stack.EmptyStackException;

public class NonOptimalSinkingStack<T> {
    private final T[] elements;
    private int size;
    private final int capacity;

    @SuppressWarnings("unchecked")
    public NonOptimalSinkingStack(int capacity) {
        this.capacity = capacity;
        this.elements = (T[]) new Object[capacity];
        this.size = 0;
    }

    public void push(T element) {
        if (size == capacity) {
            for (int i = 0; i < size - 1; i++) {
                elements[i] = elements[i + 1];
            }
            elements[size - 1] = element;
        } else {
            elements[size++] = element;
        }
    }

    public T pop() throws EmptyStackException {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        T element = elements[--size];
        elements[size] = null;
        return element;
    }

    public T peek() throws EmptyStackException {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return elements[size - 1];
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
    }