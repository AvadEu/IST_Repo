import java.io.*;
import java.util.Scanner;

public class Main {

    private static Pracownik[] pracownicy = new Pracownik[10];
    private static int liczba = 0;

    public static void main(String[] args) {

        while (true) {

            getMenu();
            Scanner sc = new Scanner(System.in);
            int choice = sc.nextInt();

            switch (choice) {
                case 1:
                    if (liczba < pracownicy.length) {
                        pracownicy[liczba] = getPracownik();
                        liczba++;
                    } else {
                        System.out.println("Maksymalna ilość pracowników");
                    }
                    break;
                case 2:
                    if (liczba + 1 < pracownicy.length) {
                        pracownicy[liczba] = new PracownikEtatowy("Jan", "Kowalski", "Dyrektor", 12332145678L, 10, 0.75, 15000);
                        pracownicy[liczba + 1] = new PracownikGodzinowy("Maciej", "Nowak", "Elektryk", 32145698789L, 2, 250, 35);
                        liczba = liczba + 2;
                    } else {
                        System.out.println("Maksymalna ilość pracowników");
                    }
                    break;
                case 3:
                    getPracownicy();
                    break;
                case 4:
                    zapiszDoPliku(pracownicy, liczba);
                    break;
                case 5:
                    odczytajPlik();
                    break;
                case 6:
                    System.out.println("Liczba pracowników: " + liczba);
                    break;
                case 7:
                    System.exit(0);
                default:
                    System.out.println("Wybrano nie poprawną opcję!");
                    break;
            }
        }
    }

    public static Pracownik getPracownik() {
        Scanner sc = new Scanner(System.in);
        System.out.println("1. Pracownik etatowy");
        System.out.println("2. Pracownik godzinowy");
        int type = sc.nextInt();
        sc.nextLine();
        System.out.println("Podaj imię: ");
        String imie = sc.nextLine();
        System.out.println("Podaj nazwisko: ");
        String nazwisko = sc.nextLine();
        System.out.println("Podaj stanowisko: ");
        String stanowisko = sc.nextLine();
        System.out.println("Podaj pesel: ");
        long pesel = sc.nextLong();
        sc.nextLine();
        System.out.println("Podaj staż: ");
        int staz = sc.nextInt();
        sc.nextLine();

        if (type == 1) {
            System.out.println("Podaj etat:");
            double etat = sc.nextDouble();
            sc.nextLine();
            System.out.println("Podaj stawkę:");
            double stawka = sc.nextDouble();
            sc.nextLine();
            return new PracownikEtatowy(imie, nazwisko, stanowisko, pesel, staz, etat, stawka);
        } else if (type == 2) {
            System.out.println("Podaj stawkę za godzinę: ");
            double stawka = sc.nextDouble();
            sc.nextLine();
            System.out.println("Podaj liczbę godzin:");
            int liczba_godz = sc.nextInt();
            sc.nextLine();
            return new PracownikGodzinowy(imie, nazwisko, stanowisko, pesel, staz, stawka, liczba_godz);
        }
        return null;
    }

    public static void getMenu() {
        System.out.println("Menu:");
        System.out.println("1. Dodaj pracownika");
        System.out.println("2. Dodaj pracowników");
        System.out.println("3. Wyświetl pracowników");
        System.out.println("4. Zapisz pracowników to pliku");
        System.out.println("5. Wczytaj pracowników z pliku");
        System.out.println("6. Podaj ilość pracowników");
        System.out.println("7. Zakończ");
    }

    public static void getPracownicy() {
        System.out.println("\n-------------------------------------------------------------------------------------------");
        System.out.printf("| %-15s | %-10s | %-12s | %-15s | %-10s | %-10s |\n", "Nazwisko", "Imię", "PESEL", "Stanowisko", "Staż", "Pensja");
        System.out.println("-------------------------------------------------------------------------------------------");

        PracownikIterator iterator = new PracownikIterator(pracownicy, liczba);

        while (iterator.hasNext()) {
            Pracownik p = iterator.next();
            p.wyświetl();
        }
        System.out.println("-------------------------------------------------------------------------------------------");
    }

    private static void zapiszDoPliku(Pracownik[] pracownicy, int iloscPracownikow) {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("pracownicy.bin"))) {
            oos.writeInt(iloscPracownikow);
            for (int i = 0; i < iloscPracownikow; i++) {
                oos.writeObject(pracownicy[i]);
            }
            System.out.println("Dane zostały zapisane do pliku pracownicy.bin");
        } catch (IOException e) {
            System.out.println("Błąd podczas zapisywania do pliku: " + e.getMessage());
        }
    }

    private static void odczytajPlik() {
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream("pracownicy.bin"))) {
            int ile_prac = ois.readInt();

            for (int i = 0; i < ile_prac; i++) {
                if (liczba < pracownicy.length) {
                    pracownicy[liczba] = (Pracownik) ois.readObject();
                    liczba++;
                } else {
                    System.out.println("Brak miejsca na pracowników!");
                    break;
                }
            }

            System.out.println("Odczytano " + ile_prac + " pracowników.");
        } catch (IOException | ClassNotFoundException e) {
            System.out.println("Błąd podczas odczytywania pliku: " + e.getMessage());
        }
    }
}
