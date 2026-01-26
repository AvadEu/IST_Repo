public class ConsumerTask2 implements Runnable {
    private final SharedBufferFIFO buffer;
    private final int id;

    public ConsumerTask2(SharedBufferFIFO buffer, int id) {
        this.buffer = buffer;
        this.id = id;
    }

    @Override
    public void run() {
        while (true) {
            int x = buffer.get();
            System.out.println("Konsument " + id + " rozpoczął " + x);
            try {
                Thread.sleep(x);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            System.out.println("Konsument " + id + " zakończył " + x);
        }
    }
}