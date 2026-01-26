public class MainTask2 {
    public static void main(String[] args) {

        int bufferSize = 5;
        SharedBufferFIFO buffer = new SharedBufferFIFO(bufferSize);

        int producerCount = 3;
        int consumerCount = 4;

        System.out.println("--- Start symulacji: " + producerCount + " Prod, "
                + consumerCount + " Kons, Bufor: " + bufferSize + " ---");

        for (int i = 1; i <= producerCount; i++) {
            new Thread(new ProducerTask2(buffer, i)).start();
        }

        for (int i = 1; i <= consumerCount; i++) {
            new Thread(new ConsumerTask2(buffer, i)).start();
        }
    }
}