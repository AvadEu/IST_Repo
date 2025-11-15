package Task1;

import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;

public class KthElementIterator<T> implements Iterator<T> {
    private final Iterator<T> baseIterator;
    private final int k;
    private int currentPosition;
    private T nextElement;
    private boolean hasNextElement;

    public KthElementIterator(Iterator<T> baseIterator, int k) {
        if (k < 1) {
            throw new IllegalArgumentException("k musi być większe lub równe 1");
        }
        this.baseIterator = baseIterator;
        this.k = k;
        this.currentPosition = 0;
        advanceToNextKthElement();
    }

    private void advanceToNextKthElement() {
        hasNextElement = false;
        while (baseIterator.hasNext()) {
            T element = baseIterator.next();
            currentPosition++;
            if (currentPosition % k == 0) {
                nextElement = element;
                hasNextElement = true;
                break;
            }
        }
    }

    @Override
    public boolean hasNext() {
        return hasNextElement;
    }

    @Override
    public T next() {
        if (!hasNextElement) {
            throw new NoSuchElementException();
        }
        T elementToReturn = nextElement;
        advanceToNextKthElement();
        return elementToReturn;
    }

    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        for (Integer num : numbers) {
            System.out.print(num + " ");
        }
        System.out.println();

        Iterator<Integer> everySecondElement = new KthElementIterator<>(numbers.iterator(), 4);
        while (everySecondElement.hasNext()) {
            System.out.print(everySecondElement.next() + " ");
        }
        System.out.println();

    }
}