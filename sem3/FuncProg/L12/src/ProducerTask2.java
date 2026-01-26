import java.util.Random;

public class ProducerTask2 implements Runnable {
    private final SharedBufferFIFO buffer;
    private final int id;
    private final Random random = new Random();

    public ProducerTask2(SharedBufferFIFO buffer, int id) {
        this.buffer = buffer;
        this.id = id;
    }

    @Override
    public void run() {
        while (true) {
            int x = 500 + random.nextInt(4501);
            buffer.put(x, id);
            try { Thread.sleep(500); } catch (InterruptedException e) {}
        }
    }
}