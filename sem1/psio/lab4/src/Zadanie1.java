import java.util.Scanner;

public class Zadanie1 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        double x = sc.nextDouble();
        double wynik = S(n,x);

        System.out.printf("S(%d, %.2f) = %.10f", n, x, wynik);
    }

    public static double S(int n, double x) {

        double outcome = 1;

        if (x < -2) {
            return Math.pow(Math.E, x);
        } else if (x >= -2 && x <= 0) {
            return 4.0/5;
        } else if (x > 0) {
            double factorial = 1;

            for (int i = 1; i <= n; i++) {
                factorial = factorial * i;
                outcome *= ((x+i) / factorial);
            }
        }
        return outcome;
    }
}
