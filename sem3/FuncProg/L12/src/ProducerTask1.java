import java.util.Random;

public class ProducerTask1 implements Runnable {
    private final SharedBufferOne buffer;
    private final Random random = new Random();

    public ProducerTask1(SharedBufferOne buffer) {
        this.buffer = buffer;
    }

    @Override
    public void run() {
        while (true) {
            int x = 500 + random.nextInt(4501);
            buffer.put(x);
        }
    }
}