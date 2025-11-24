import java.util.Random;

public class Zad2 {
    public static void main(String[] args) {
        Random rand = new Random();
        int[] A = new int[20];
        int[] B = new int[20];

        for (int i = 0; i < A.length; i++) {
            A[i] = rand.nextInt(101) - 100;
            B[i] = rand.nextInt(101) - 100;
        }

        for (int i = 0; i < A.length; i++) {
            int s = A[i] + B[i];
            int d = A[i] - B[i];
            int m = A[i] * B[i];
            System.out.printf("a[ %2d ]=%5d  b[ %2d ]= %5d   ", i, A[i], i, B[i]);
            System.out.printf("su=%5d   ro=%5d   il=%5d   max=%5d%n", s, d, m, maxOfThree(s, d, m));

        }
    }

    public static int maxOfThree(int a, int b, int c) {
        return Math.max(Math.max(a, b), c);
    }
}
