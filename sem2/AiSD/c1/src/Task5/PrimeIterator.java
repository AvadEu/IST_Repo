package Task5;

import java.util.Iterator;
import java.util.NoSuchElementException;

public class PrimeIterator implements Iterator<Integer> {

    private final int limit;
    private int current;
    private final boolean[] primes;

    public PrimeIterator(int limit) {
        this.limit = limit;
        this.current = 2;
        primes = sieve();
    }

    public boolean hasNext() {
        for (int i = current; i < limit; i++) {
            if (primes[i]) return true;
        }
        return false;
    }

    public Integer next() {
        if (!hasNext()) {
        throw new NoSuchElementException();
        }
        for (int i = current; i < limit; i++) {
            if (primes[i]) {
                current = i + 1;
                return i;
            }
        }
        throw new NoSuchElementException();
    }

    private boolean[] sieve() {
        boolean[] prime = new boolean[limit+1];

        for(int i=0; i<=limit; i++) {
            prime[i] = true;
        }

        for(int p = 2; p*p <=limit; p++)
        {
            if (prime[p])
            {
                for(int i = p*p; i <= limit; i += p)
                    prime[i] = false;
            }
        }
        return prime;
    }

    public static void main(String[] args) {
        PrimeIterator primeIterator = new PrimeIterator(1000);
        while (primeIterator.hasNext()) {
            System.out.print(primeIterator.next() + " ");
        }
    }
}
