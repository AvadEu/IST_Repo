public class Zadanie2 {
    public static void main(String[] args) {
        int n = 2, m = 20;
        int suma = 0;

        if (n < m) {

            int i;

            if (n % 2 == 0) {
                i = n;
            } else {
                i = n + 1;
            }

            while (i <= m) {
                suma = suma + i;
                i = i + 2;
            }

            System.out.println("Suma wynosi: " + suma);
        } else {
            System.out.println("Nie da się obliczyć sumy!");
        }
    }
}
