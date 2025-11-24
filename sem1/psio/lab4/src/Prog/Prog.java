package Prog;
import Wielomian.Wielomian;

public class Prog {
    public static void main(String[] args) {
        int n = 3;
        double x = 3.5;
        Wielomian wielomian = new Wielomian();

        double wynik = wielomian.Czebyszew(n, x);

        System.out.printf("T(%d) = %.3f\n", n, wynik);
    }
}
