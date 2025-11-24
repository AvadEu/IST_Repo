public class Triangle {
    public static void main(String[] args) {
        double a = 1, b = 1, c = 2;

        if (!(Math.abs(b - c) < a && a < b + c)) {
            System.out.printf("Trójkąt o bokach: %2.2f, %2.2f, %2.2f nie istnieje!\n", a, b, c);
            System.exit(0);
        }

        double p = (a + b + c) / 2;
        double area = Math.sqrt(p * (p - a) * (p - b) * (p - c));
        System.out.printf("Trójkąt o bokach %2.2f, %2.2f ,%2.2f ma pole=%2.2f\n", a, b, c, area);



    }
}
