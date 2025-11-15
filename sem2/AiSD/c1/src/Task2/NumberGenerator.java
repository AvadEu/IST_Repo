package Task2;

import java.util.Iterator;
import java.util.NoSuchElementException;

public class NumberGenerator implements Iterator<Integer> {

    private int current;

    public NumberGenerator(int start) {
        this.current = start;
    }

    public boolean hasNext() {
        return true;
    }

    public Integer next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
            return current++;
    }

    public void remove() {
        throw new UnsupportedOperationException();
    }

    public static void main(String[] args) {
        Iterator<Integer> numberGenerator  = new NumberGenerator(10);
        while (numberGenerator.hasNext()) {
            int n = numberGenerator.next();
            System.out.print(n + " ");
            if (n == 20) {
                break;
            }
        }
    }
}