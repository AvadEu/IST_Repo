public class Main {
    public static void main(String[] args) {

        int a = 4, b = 7;

        int area = a * b; // Pole
        int ob = 2 * a + 2 * b; // Obwód
        double diag = Math.sqrt(a * a + b * b); // Przekątna

        System.out.printf("Boki prostokąta: a=%d b=%d%n", a, b);
        System.out.println("Pole=" + area);
        System.out.println("Obwód=" + ob);
        System.out.printf("Przekątna=%.2f%n", diag);

        System.out.println();
        int r = 5;

        double area2 = Math.PI * r * r;
        double ob2 = 2 * Math.PI * r;

        System.out.printf("Promień koła = %d%n", r);
        System.out.printf("Pole koła = %.3f%n", area2);
        System.out.printf("Obwód koła = %.3f%n", ob2);

    }
}