import java.util.Scanner;

public class Figury {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        boolean czyKoniec = false;

        while (!czyKoniec) {
            System.out.printf("'K': Kula%n'P' Prostopadłościan%n'S': Stop%n");
            String w = sc.nextLine();

            switch (w) {
                case "K":
                    System.out.println("Podaj promień kuli:");
                    double r = sc.nextDouble();
                    sc.nextLine(); // Zbieranie pozostałości

                    System.out.printf("Objętość kuli: %.5f%n", VolumeKula(r));
                    System.out.printf("Pole powierzchni kuli: %.5f%n", SurfaceKula(r));
                    break;
                case "P":
                    System.out.println("Podaj wymiary a, b, c:");
                    double a = sc.nextDouble(), b = sc.nextDouble(), c = sc.nextDouble();
                    sc.nextLine(); // Zbieranie pozostałości

                    System.out.printf("Objętość prostopadłościanu: %.5f%n", VolumeCuboid(a, b, c));
                    System.out.printf("Pole powierzchni prostopadłościanu: %.5f%n", SurfaceCuboid(a, b, c));
                    break;
                case "S":
                    czyKoniec = true;
                    break;
                default:
                    System.out.println("Wprowadź poprawną opcję!");
                    break;
            }
        }
    }

    public static double VolumeKula(double r) {
        return 4.0 / 3.0 * Math.PI * Math.pow(r, 3);
    }

    public static double VolumeCuboid(double a, double b, double c) {
        return a * b * c;
    }

    public static double SurfaceKula(double r) {
        return 4 * Math.PI * Math.pow(r, 2);
    }

    public static double SurfaceCuboid(double a, double b, double c) {
        return 2 * a * b + 2 * b * c + 2 * a * c;
    }
}
