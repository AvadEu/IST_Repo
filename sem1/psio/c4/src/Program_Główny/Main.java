package Program_Główny;

import Biblioteka.Maths;

public class Main {

    public static void main(String[] args) {

        double x = Math.PI / 4;
        int n = 5;

        System.out.println("Przybliżenie sin(" + x + ") = " + Maths.sin(x, n));

        System.out.println("Przybliżenie cos(" + x + ") = " + Maths.cos(x, n));

        double expInput = 3.0;
        System.out.println("Przybliżenie e^" + expInput + " = " + Maths.exp(expInput, n));
    }
}
