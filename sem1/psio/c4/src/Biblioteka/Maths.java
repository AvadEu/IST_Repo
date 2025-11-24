package Biblioteka;

public class Maths {

    public static double sin(double x, int n) {
        double result = 0;
        for (int i = 0; i < n; i++) {
            double term = Math.pow(-1, i) * Math.pow(x, 2 * i + 1) / factorial(2 * i + 1);
            result += term;
        }
        return result;
    }

    public static double cos(double x, int n) {
        double result = 0;
        for (int i = 0; i < n; i++) {
            double term = Math.pow(-1, i) * Math.pow(x, 2 * i) / factorial(2 * i);
            result += term;
        }
        return result;
    }

    public static double exp(double x, int n) {
        double result = 0;
        for (int i = 0; i < n; i++) {
            result += Math.pow(x, i) / factorial(i);
        }
        return result;
    }

    public static double factorial(int n) {
        int f = 1;
        for (int i = 1; i <= n; i++) {
            f *= i;
        }
        return f;
    }
}
