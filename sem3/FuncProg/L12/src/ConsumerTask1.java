public class ConsumerTask1 implements Runnable {
    private final SharedBufferOne buffer;
    private final int id;

    public ConsumerTask1(SharedBufferOne buffer, int id) {
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