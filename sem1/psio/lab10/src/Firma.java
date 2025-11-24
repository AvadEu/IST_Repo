import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;
import java.util.Scanner;

public class Firma {

    public static Wypłata[] wynagordzenia = new Wypłata[100];
    private static Random rand = new Random();

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        while (true) {
            displayMenu();
            int choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                    dodajWieleWypłat();
                    break;
                case 2:
                    wyświetlWypłaty();
                    break;
                case 3:
                    dodajWypłatę();
                    break;
                case 4:
                    System.out.printf("Wypłat z kartą kierownika: %2d%n", ileWypłatZKartąKierownika());
                    break;
                case 5:
                    personelZNajmniejsząWypłatą();
                    break;
                case 6:
                    zapiszWypłaty();
                    break;
                case 7:
                    System.exit(0);
                    break;
                default:
                    System.out.println("Wybrano nie poprawną opcję!");
                    break;
            }

        }
//        dodajWieleWypłat();
//        wyświetlWypłaty();
    }

    private static void displayMenu() {
        System.out.println("Wybierz czynność:");
        System.out.println("1 - Wstaw kilka wypłat z różnymi kartami.");
        System.out.println("2 - Wyświetl utworzone wypłaty.");
        System.out.println("3 - Dodaj jedną wypłatę.");
        System.out.println("4 - Policz wypłaty z kartą kierownika.");
        System.out.println("5 - Wyświetl pracownika z KartąPersonelu o najniższej wypłacie.");
        System.out.println("6 - Zapisz do pliku wypłaty z użyciem KartyPersonelu");
        System.out.println("7 - Zakończ");

    }

    private static void wyświetlWypłaty() {
        for (int i = 0; i < wynagordzenia.length; i++) {
            if (wynagordzenia[i] != null) {
                System.out.println(wynagordzenia[i].toString());
            } else {
                break;
            }
        }
    }

    private static void dodajWieleWypłat() {
        KartaPracownika karty[] = new KartaPracownika[5];
        karty[0] = new KartaPersonelu(10, "Nowak");
        karty[1] = new KartaPersonelu(11, "Wesoły");
        karty[2] = new KartaKierownika(20, "Kraśny");
        karty[3] = new KartaKierownika(21, "Kowalski");
        karty[4] = new KartaDyrektora(31, "Lewandowski");
        for (int i = 0; i < karty.length; i++) {
            for (int j = 0; j < 3; j++) {
                int pensja = rand.nextInt(4000, 10001);
                dodajWypłatęDoWynagrodzenia(new Wypłata(pensja, karty[i]));
            }
        }

    }

    private static void dodajWypłatę() {
        Scanner sc = new Scanner(System.in);

        System.out.println("Podaj pensję: ");
        int pensja = sc.nextInt();
        sc.nextLine();

        int numer = rand.nextInt(10000, 100000);

        System.out.println("Podaj Nazwisko: ");
        String nazwisko = sc.nextLine();

        System.out.printf("Wybierz stopień: %n1 - Dyrektor%n2 - Kierownik%n3 - Personel%n");
        int stopien = sc.nextInt();
        sc.nextLine();

        KartaPracownika k = null;

        switch (stopien) {
            case 1:  k = new KartaDyrektora(numer, nazwisko);
            break;
            case 2:  k = new KartaKierownika(numer, nazwisko);
            break;
            case 3:  k = new KartaPersonelu(numer, nazwisko);
            break;
        }

        Wypłata w = new Wypłata(pensja, k);

        dodajWypłatęDoWynagrodzenia(w);
    }

    private static void dodajWypłatęDoWynagrodzenia(Wypłata w) {
        for (int i = 0; i < wynagordzenia.length; i++) {
            if (wynagordzenia[i] == null) {
                wynagordzenia[i] = w;
                break;
            }
        }
    }

    private static int ileWypłatZKartąKierownika() {
        int licznik = 0;
        for (int i = 0; i < wynagordzenia.length; i++) {
            if ((wynagordzenia[i] != null) && (wynagordzenia[i].getKarta() instanceof KartaKierownika)) {
                    licznik++;
            }
        }
        return licznik;
    }

    private static void personelZNajmniejsząWypłatą() {
        double min_w = Double.MAX_VALUE;
        KartaPracownika k = null;
        for (int i = 0; i < wynagordzenia.length; i++) {
            if ((wynagordzenia[i] != null) && (wynagordzenia[i].getKarta() instanceof KartaPersonelu)) {
                if (wynagordzenia[i].pensjaZPremia() < min_w) {
                    min_w = wynagordzenia[i].pensjaZPremia();
                    k = wynagordzenia[i].getKarta();
                }
            }
        }
        if (k != null) {
            System.out.printf("Najmniej dostał: %s (%f)%n", k.toString(), min_w);
        } else {
            System.out.println("Brak pracowników personelu!");
        }
    }

    private static void zapiszWypłaty() {
        try {

            FileWriter fw = new FileWriter("baza.txt");
            BufferedWriter bw = new BufferedWriter(fw);

            for (int i = 0; i < wynagordzenia.length; i++) {
                if (wynagordzenia[i] != null && (wynagordzenia[i].getKarta() instanceof KartaPersonelu)) {
//                    bw.write(1);
                    bw.write(wynagordzenia[i].toString());
                    bw.newLine();
                }
            }
            bw.close();
            System.out.println("Pomyślnie zapisano do pliku!");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}