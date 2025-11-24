package Wielomian;

public class Wielomian {
    public static double Czebyszew(int n, double x) {

        if ( n == 0) {
            return 1.0;
        } else if ( n == 1) {
            return x;
        }

        double T0 = 1, T1 = x, Tn = 0;

        for (int i = 2; i <= n; i++) {
            Tn = 2 * x * T1 - T0;
            T0 = T1;
            T1 = Tn;
        }
        return Tn;
    }
}
