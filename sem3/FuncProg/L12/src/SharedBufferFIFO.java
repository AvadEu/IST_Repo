import java.util.LinkedList;
import java.util.Queue;
import java.util.concurrent.Semaphore;

public class SharedBufferFIFO {
    private final Queue<Integer> queue;
    private final Semaphore spaces;
    private final Semaphore items;
    private final Semaphore mutex;

    public SharedBufferFIFO(int capacity) {
        this.queue = new LinkedList<>();
        this.spaces = new Semaphore(capacity);
        this.items = new Semaphore(0);
        this.mutex = new Semaphore(1);
    }

    public void put(int x, int producerId) {
        try {
            spaces.acquire();
            mutex.acquire();

            queue.add(x);
            System.out.println("Producent " + producerId + " wyprodukował " + x);

            mutex.release();
            items.release();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    public int get() {
        int x = 0;
        try {
            items.acquire();
            mutex.acquire();

            try {
                x = queue.poll();
            } catch (NullPointerException e) {
                Thread.currentThread().interrupt();
            }

            mutex.release();
            spaces.release();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return x;
    }
}