import java.util.concurrent.Semaphore;

public class SharedBufferOne {
    private int value;
    private final Semaphore empty = new Semaphore(1);
    private final Semaphore full = new Semaphore(0);

    public void put(int x) {
        try {
            empty.acquire();
            this.value = x;
            full.release();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    public int get() {
        int result = 0;
        try {
            full.acquire();
            result = this.value;
            empty.release();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return result;
    }
}