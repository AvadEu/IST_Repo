public class MainTask1 {
    public static void main(String[] args) {
        SharedBufferOne buffer = new SharedBufferOne();

        Thread producer = new Thread(new ProducerTask1(buffer));
        producer.start();

        int numberOfConsumers = 3;
        for (int i = 1; i <= numberOfConsumers; i++) {
            new Thread(new ConsumerTask1(buffer, i)).start();
        }
    }
}