public class Eksperyment {
    public static void main(String[] args) {
        long startTime, gen1 = 0, gen2 = 0, dec1 = 0, dec2 = 0;
        for (int i = 0; i < 10000; i++) {
            startTime = System.nanoTime();
            genException1();
            gen1 = System.nanoTime() - startTime;

            startTime = System.nanoTime();
            genException2();
            gen2 = System.nanoTime() - startTime;

            startTime = System.nanoTime();
            try {
                decException1();
            } catch (ArithmeticException e) {
                e.toString();
            }
            dec1 = System.nanoTime() - startTime;

            startTime = System.nanoTime();
            try {
                decException2();
            } catch (ArrayIndexOutOfBoundsException e) {
                e.toString();
            }
            dec2 = System.nanoTime() - startTime;
            System.out.printf("%d %d %d %d%n", gen1, gen2, dec1, dec2);
        }
    }

    public static void genException1() {
        int n = 0;
        try {
            int k = 1 / 0;
        } catch (ArithmeticException e) {
            n += 1;
        }
    }

    public static void genException2() {
        int n = 0;
        int[] arr = new int[3];
        try {
            arr[3] = 5;
        } catch (ArrayIndexOutOfBoundsException e) {
            n += 1;
        }
    }

    public static void decException1() throws ArithmeticException {
        int n = 0;
        n = n / 0;
    }

    public static void decException2() throws ArrayIndexOutOfBoundsException {
        int[] arr = new int[3];
        arr[3] = 5;
    }
}
