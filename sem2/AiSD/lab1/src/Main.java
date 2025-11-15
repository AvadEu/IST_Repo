import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;

public class Main {

    private static ArrayList<Karta> karty = new ArrayList<>();

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        while (true) {
            displayMenu();
            int choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                    karty.clear();
                    getKarty();
                    System.out.println("Utworzono listę kart.");
                    break;
                case 2:
                    System.out.println("Karty:");
                    displayKarty();
                    break;
                case 3:
                    System.out.println("Ilość kart: " + karty.size());
                    break;
                case 4:
                    System.out.println("Podaj wartość: ");
                    int wartosc = sc.nextInt();
                    sc.nextLine();
                    ValueFilter.apply(karty, wartosc);
                    break;
                case 5:
                    System.out.println("Podaj kolor: ");
                    int color = sc.nextInt();
                    sc.nextLine();
                    ColorFilter.apply(karty, color);
                    break;
                case 6:
                    System.out.println("Dodano 3 asy kier!");
                    karty.add(0, new Karta(1, 0));
                    karty.add(0, new Karta(1, 0));
                    karty.add(0, new Karta(1, 0));
                    displayKarty();
                    System.out.println("Usuwanie duplikatów...");
                    karty = usuńDuplikaty();
                    System.out.println("Duplikaty zostały usunięte!");
                    break;
                case 7:
                    System.exit(0);
                default:
                    System.out.println("Wybrano niepoprawną opcję");
            }

        }

    }

    public static void displayMenu() {
        System.out.println("Menu:");
        System.out.println("1. Utworzenie ArrayList");
        System.out.println("2. Wyświetlenie wszystkich elementów");
        System.out.println("3. Wyświetlenie liczby elementów");
        System.out.println("4. Wyświetlanie kart o podaje wartości");
        System.out.println("5. Wyświetlenie kart o podanym kolorze");
        System.out.println("6. Usuwanie kart powtarzających się");
        System.out.println("7. Zakończ");
    }

    public static void getKarty() {
        Random rand = new Random();
        int wartosc = rand.nextInt(14);

        while (wartosc != 0) {
            Karta nowa_karta = new Karta(wartosc, rand.nextInt(4));

            int index = 0;

            for (Karta karta : karty) {
                if (!czyPrzed(nowa_karta, karta)) {
                    index++;
                }
            }
            wartosc = rand.nextInt(14);
            karty.add(index, nowa_karta);
        }

    }

    public static boolean czyPrzed(Karta k1, Karta k2) {
        return (k1.getWartosc() < k2.getWartosc() ||
                (k1.getWartosc() == k2.getWartosc() && k1.getKolor() < k2.getKolor()));
    }

    public static void displayKarty() {
        for (Karta karta: karty) {
            System.out.println(karta.toString());
        }
    }

    public static ArrayList<Karta> usuńDuplikaty() {
        ArrayList<Karta>  unique = new ArrayList<>();
        for (Karta karta: karty) {
            if (!unique.contains(karta)) {
                unique.add(karta);
            }
        }
        return unique;
    }
}