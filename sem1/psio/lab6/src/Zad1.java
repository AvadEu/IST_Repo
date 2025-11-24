import java.util.Random;

public class Zad1 {
    public static void main(String [] args) {
        Random rand = new Random();

        int[] A = new int[20];

        for (int i = 0; i < A.length; i++) {
            A[i] = rand.nextInt(201) - 100;
        }

        int maxElement = -101;
        int maxIndex = -1;

        for (int i = 0; i < A.length; i++) {
            if (A[i] >= maxElement) {
                maxElement = A[i];
                maxIndex = i;
            }
        }
        System.out.println("pozycja=" + maxIndex);

        for (int i = 0; i < A.length; i++) {
            System.out.printf("a[%2d]=%d\n", i, A[i]);
        }
    }
}
