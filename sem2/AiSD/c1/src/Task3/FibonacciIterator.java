package Task3;

import java.util.Iterator;
import java.util.NoSuchElementException;

public class FibonacciIterator implements Iterator<Integer> {
    private int previous;
    private int current;

    public FibonacciIterator() {
        this.previous = 0;
        this.current = 1;
    }

    public boolean hasNext() {
        return true;
    }

    public Integer next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        int result = current;
        int next = previous + current;
        previous = current;
        current = next;
        return result;
    }

    public void remove() {
        throw new UnsupportedOperationException();
    }

    public static void main(String[] args) {
        FibonacciIterator fib = new FibonacciIterator();
        int elemsCount = 10;
        int howMany = 0;
        while (fib.hasNext()) {
            System.out.print(fib.next() + " ");
            if (howMany++ > elemsCount) break;

        }
    }
}
