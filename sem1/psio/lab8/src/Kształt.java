import Kształty.Bryła;
import Kształty.Prostopadłościan;
import Kształty.Walec;

import java.util.Random;

public class Kształt {

    static Random rand = new Random();

    static Bryła [] tablica = new Bryła[20];
    static int n = 0;

    public static void main(String[] args) {

        // Wstawia x prostopadłościanów
        int ile_prostopadloscianow = 5;
        for (int i = 0; i < ile_prostopadloscianow; i++) {
            n++;
            int a = rand.nextInt(20) + 1;
            int b = rand.nextInt(20) + 1;
            int h = rand.nextInt(20) + 1;
            tablica[i] = new Prostopadłościan(String.format("Pr: %d", i + 1), a, b, h);
        }
        System.out.println();

        // Wstawia y walców
        int ile_walcow = 5;
        for (int i = n; i < ile_prostopadloscianow + ile_walcow; i++) {
            n++;
            int r = rand.nextInt(20) + 1;
            int h = rand.nextInt(20) + 1;
            tablica[i] = new Walec(String.format("W: %d", n), h, r);
        }
        System.out.println();

        // Konstruktory domyślne
        tablica[n] = new Walec();
        tablica[n + 1] = new Prostopadłościan();
        n += 2;

        // Wyświetla największe pole
        int index = -1;
        double max_pole = -1;
        for (int i = 0; i < n; i++) {
            if (tablica[i].Pole() > max_pole) {
                max_pole = tablica[i].Pole();
                index = i;
            }
        }
        System.out.printf("Największe pole ma %s: %s na pozycji %d w tablicy.%n",
                tablica[index].getClass().getSimpleName(), tablica[index].getNazwa(), index);
        System.out.println();

        // Wyświetla kolejno wszystkie bryły
        for (int i = 0; i < n; i++) {
            System.out.println(tablica[i].toString());
        }
        System.out.println();

        // Wyświetla same walce
        for (int i = 0; i < n; i++) {
            if (tablica[i] instanceof Walec) {
                System.out.println(tablica[i].toString());
            }
        }
        System.out.println();

        // Wyświetla same prostopadłościany
        for (int i = 0; i < n; i++) {
            if (tablica[i] instanceof Prostopadłościan) {
                System.out.println(tablica[i].toString());
            }
        }
        System.out.println();

        // Wyświetla liczbę sześcianów
         tablica[0] = new Prostopadłościan("Przykład", 2, 2, 2);
        int liczba_sześcianów = 0;
        for (int i = 0; i < n; i++) {
            if (tablica[i] instanceof Prostopadłościan &&  ((Prostopadłościan)tablica[i]).jestSześcianem()) {
                    liczba_sześcianów++;
            }
        }
        System.out.println("Liczba sześcianów to: " + liczba_sześcianów);
        System.out.println();

        // Wyświetla liczbę walców stworzonych z kwadratu
         tablica[5] = new Walec("Przykład", 2, 1);
        int x = 0;
        for (int i = 0; i < n; i++) {
            if (tablica[i] instanceof Walec && ((Walec) tablica[i]).obrótKwadratu()) {
                x++;
            }
        }
        System.out.println("Liczba walców powstałych z kwadratu to: " + x);
    }
}