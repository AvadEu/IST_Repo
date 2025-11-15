import java.util.Random;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        OneWayLinkedListWithHead<Karta> listaKart = new OneWayLinkedListWithHead<Karta>();
        boolean[] duplikaty = new boolean[52];

        Scanner sc = new Scanner(System.in);

        while (true) {
            System.out.println("Menu:");
            System.out.println("1. Tworzenie listy");
            System.out.println("2. Wyświetlanie listy");
            System.out.println("3. Wyświetlanie liczby elementów");
            System.out.println("4. Wyświetlanie kart o podanej wartości");
            System.out.println("5. Wyświetlanie kart o podanym kolorze");
            System.out.println("6. Usuwanie kart zakrytych");
            System.out.println("7. Zakończ program");

            int wybor = sc.nextInt();
            sc.nextLine();

            switch (wybor) {
                case 1:
                    tworzenieListy(listaKart, duplikaty);
                    break;
                case 2:
                    System.out.println(listaKart);
                    break;
                case 3:
                    getSize(listaKart);
                    break;
                case 4:
                    System.out.print("Podaj wartość karty (1-13): ");
                    int wartosc = sc.nextInt();
                    sc.nextLine();
                    wyswietlKartyPoWartosci(listaKart, wartosc);
                    break;
                case 5:
                    System.out.print("Podaj kolor karty (0-kier, 1-karo, 2-trefl, 3-pik): ");
                    int kolor = sc.nextInt();
                    sc.nextLine();
                    wyswietlKartyPoKolorze(listaKart, kolor);
                    break;
                case 6:
                    usuwanieKartZakrytych(listaKart);
                    break;
                case 7:
                    System.exit(0);
                    break;
                default:
                    System.out.println("Nieprawidłowy wybór.");
                    break;
            }
        }
    }

    private static void tworzenieListy(OneWayLinkedListWithHead<Karta> listaKart, boolean[] tablicaDuplikatow) {
        Random random = new Random();

        while (true) {
            int wartosc = random.nextInt(15);
            int kolor = random.nextInt(4);

            if (wartosc == 0) break;

            boolean odkryta = wartosc <= 13;
            int id = kolor * 13 + wartosc - 1;

            if (odkryta && tablicaDuplikatow[id]) continue;

            Karta karta = new Karta(wartosc, kolor, odkryta);

            if (odkryta) {
                listaKart.addSorted(karta);
                tablicaDuplikatow[id] = true;
            } else {
                listaKart.addToEnd(karta);
            }
        }
        System.out.println("Lista została utworzona.");
    }

    private static void wyswietlKartyPoWartosci(OneWayLinkedListWithHead<Karta> listaKart, int wartosc) {
        for (Karta karta : listaKart) {
            if (wartosc == karta.getWartosc() && karta.isOdkryta()) {
                System.out.println(karta);
            }
        }
    }

    private static void wyswietlKartyPoKolorze(OneWayLinkedListWithHead<Karta> listaKart, int kolor) {
        for (Karta karta : listaKart) {
            if (karta.getKolor() == kolor && karta.isOdkryta()) {
                System.out.println(karta);
            }
        }
    }

    private static void usuwanieKartZakrytych(OneWayLinkedListWithHead<Karta> listaKart) {
        listaKart.removeHiddenCards();
        System.out.println("Zakryte karty zostały usunięte.");
    }

    public static void getSize(OneWayLinkedListWithHead<Karta> listaKart) {
        int liczba_kart = listaKart.size();
        int liczba_zakrytych = 0;
        for (Karta karta : listaKart) {
            if (!karta.isOdkryta()) liczba_zakrytych++;
        }
        int liczba_odkrytych = liczba_kart - liczba_zakrytych;
        System.out.println("Łączna liczba kart: " + liczba_kart);
        System.out.println("Karty odkryte: " + liczba_odkrytych);
        System.out.println("Karty zakryte: " + liczba_zakrytych);
    }
}
