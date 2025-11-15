import java.io.*;
import java.util.Comparator;
import java.util.Scanner;

public class Main {
    private static L2KCzS<Auto> baza = new L2KCzS<>();
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        while (true) {
            wyswietlMenu();
            int wybor = scanner.nextInt();
            scanner.nextLine();

            switch (wybor) {
                case 0:
                    scanner.close();
                    System.exit(0);
                    break;
                case 1:
                    utworzNowaBaze();
                    break;
                case 2:
                    odczytBazyZPliku();
                    break;
                case 3:
                    wyswietlWszystkieSamochody();
                    break;
                case 4:
                    wyswietlDaneJednegoSamochodu();
                    break;
                case 5:
                    dopiszNowySamochod();
                    break;
                case 6:
                    usunSamochodZBazy();
                    break;
                case 7:
                    aktualizujDaneSamochodu();
                    break;
                case 8:
                    wyswietlSamochodyOPodanejMarce();
                    break;
                case 9:
                    wyswietlSamochodyPonizejCeny();
                    break;
                case 10:
                    zapiszBazeDoPliku();
                    break;
                case 11:
                    symulujParking();
                    break;
                default:
                    System.out.println("Nieprawidłowy wybór.");
            }
        }
    }

    private static void wyswietlMenu() {
        System.out.println("\n=== Menu ===");
        System.out.println("1. Utworzenie nowej bazy danych");
        System.out.println("2. Odczyt bazy z pliku");
        System.out.println("3. Wyświetlenie wszystkich rekordów");
        System.out.println("4. Wyświetlenie danych jednego samochodu");
        System.out.println("5. Dopisanie nowego samochodu");
        System.out.println("6. Usunięcie samochodu z bazy");
        System.out.println("7. Aktualizowanie danych samochodu");
        System.out.println("8. Wyświetlanie danych samochodów o podanej marce");
        System.out.println("9. Wyświetlanie danych samochodów o cenach poniżej x");
        System.out.println("10. Zapis bazy do pliku (serializacja)");
        System.out.println("11. Symulacja parkingu");
        System.out.println("0. Koniec programu");
        System.out.print("Wybierz opcję: ");
    }

    private static void utworzNowaBaze() {
        baza = new L2KCzS<>();
        Auto s1 = new Auto(1, "Opel", "Kombi", "1999", 9900, "Zielony", 5);
        baza.addSorted(s1, Comparator.comparingInt(Auto::getNrSilnika));
        System.out.println("Utworzono nową bazę danych.");
    }

    private static void odczytBazyZPliku() {
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream("baza.bin"))) {
            baza = (L2KCzS<Auto>) ois.readObject();
            System.out.println("Baza danych została wczytana z pliku.");
        } catch (IOException | ClassNotFoundException e) {
            System.out.println("Błąd podczas odczytu pliku: " + e.getMessage());
        }
    }

    private static void wyswietlWszystkieSamochody() {
        if (baza.isEmpty()) {
            System.out.println("Baza danych jest pusta.");
            return;
        }

        System.out.println("Lista wszystkich samochodów:");
        for (int i = 0; i < baza.size(); i++) {
            System.out.println("\n--- Samochód " + (i+1) + " ---");
            System.out.println(baza.get(i));
        }
    }

    private static void wyswietlDaneJednegoSamochodu() {
        if (baza.isEmpty()) {
            System.out.println("Baza danych jest pusta.");
            return;
        }

        System.out.print("Podaj numer silnika samochodu: ");
        int nrSilnika = scanner.nextInt();
        scanner.nextLine();

        boolean znaleziono = false;
        for (int i = 0; i < baza.size(); i++) {
            Auto auto = baza.get(i);
            if (auto.getNrSilnika() == nrSilnika) {
                System.out.println("\nDane samochodu:");
                System.out.println(auto);
                znaleziono = true;
                break;
            }
        }

        if (!znaleziono) {
            System.out.println("Nie znaleziono samochodu o podanym numerze silnika.");
        }
    }

    private static void dopiszNowySamochod() {
        System.out.println("Dodawanie nowego samochodu:");

        System.out.print("Numer silnika: ");
        int nrSilnika = scanner.nextInt();
        scanner.nextLine();

        for (int i = 0; i < baza.size(); i++) {
            if (baza.get(i).getNrSilnika() == nrSilnika) {
                System.out.println("Samochód o podanym numerze silnika już istnieje!");
                return;
            }
        }

        System.out.print("Marka: ");
        String marka = scanner.nextLine();

        System.out.print("Typ: ");
        String typ = scanner.nextLine();

        System.out.print("Data produkcji: ");
        String dataProdukcji = scanner.nextLine();

        System.out.print("Cena: ");
        double cena = scanner.nextDouble();
        scanner.nextLine();

        System.out.print("Kolor: ");
        String kolor = scanner.nextLine();

        System.out.print("Składowanie (liczba miesięcy): ");
        int skladowanie = scanner.nextInt();
        scanner.nextLine();

        Auto nowyAuto = new Auto(nrSilnika, marka, typ, dataProdukcji, cena, kolor, skladowanie);

        baza.addSorted(nowyAuto, Comparator.comparingInt(Auto::getNrSilnika));

        System.out.println("Dodano nowy samochód do bazy.");
    }

    private static void usunSamochodZBazy() {
        if (baza.isEmpty()) {
            System.out.println("Baza danych jest pusta.");
            return;
        }

        System.out.print("Podaj numer silnika samochodu do usunięcia: ");
        int nrSilnika = scanner.nextInt();
        scanner.nextLine();

        for (int i = 0; i < baza.size(); i++) {
            Auto auto = baza.get(i);
            if (auto.getNrSilnika() == nrSilnika) {
                baza.remove(auto);
                System.out.println("Usunięto samochód z bazy.");
                return;
            }
        }

        System.out.println("Nie znaleziono samochodu o podanym numerze silnika.");
    }

    private static void aktualizujDaneSamochodu() {
        if (baza.isEmpty()) {
            System.out.println("Baza danych jest pusta.");
            return;
        }

        System.out.print("Podaj numer silnika samochodu do aktualizacji: ");
        int nrSilnika = scanner.nextInt();
        scanner.nextLine();

        boolean znaleziono = false;
        for (int i = 0; i < baza.size(); i++) {
            Auto auto = baza.get(i);
            if (auto.getNrSilnika() == nrSilnika) {
                System.out.println("1. Aktualizacja czasu składowania:");
                System.out.println("2. Aktualizacja ceny");
                System.out.println("3. Aktualizacja kolor");
                int choice = scanner.nextInt();
                scanner.nextLine();

                switch (choice) {
                    case 1:
                        System.out.print("Nowa liczba miesięcy składowania: ");
                        int noweSkladowanie = scanner.nextInt();
                        scanner.nextLine();
                        auto.setSkladowanie(noweSkladowanie);
                        System.out.println("Zaktualizowano dane samochodu.");
                    break;
                    case 2:
                        System.out.println("Nowa cena: ");
                        int noweCena = scanner.nextInt();
                        scanner.nextLine();
                        auto.setCena(noweCena);
                        System.out.println("Zaktualizowano dane samochodu.");
                    break;
                    case 3:
                        System.out.println("Nowy kolor: ");
                        String nowyKolor = scanner.nextLine();
                        auto.setKolor(nowyKolor);
                        System.out.println("Zaktualizowano dane samochodu.");
                    break;
                }

                znaleziono = true;
                break;
            }
        }

        if (!znaleziono) {
            System.out.println("Nie znaleziono samochodu o podanym numerze silnika.");
        }
    }

    private static void wyswietlSamochodyOPodanejMarce() {
        if (baza.isEmpty()) {
            System.out.println("Baza danych jest pusta.");
            return;
        }

        System.out.print("Podaj markę samochodów do wyświetlenia: ");
        String marka = scanner.nextLine();

        boolean znaleziono = false;
        System.out.println("\nSamochody marki " + marka + ":");

        for (int i = 0; i < baza.size(); i++) {
            Auto auto = baza.get(i);
            if (auto.getMarka().equalsIgnoreCase(marka)) {
                System.out.println("\n--- Samochód " + (i+1) + " ---");
                System.out.println(auto);
                znaleziono = true;
            }
        }

        if (!znaleziono) {
            System.out.println("Nie znaleziono samochodów o podanej marce.");
        }
    }

    private static void wyswietlSamochodyPonizejCeny() {
        if (baza.isEmpty()) {
            System.out.println("Baza danych jest pusta.");
            return;
        }

        System.out.print("Podaj maksymalną cenę: ");
        double maxCena = scanner.nextDouble();
        scanner.nextLine();

        boolean znaleziono = false;
        System.out.println("\nSamochody o cenie poniżej " + maxCena + ":");

        for (int i = 0; i < baza.size(); i++) {
            Auto auto = baza.get(i);
            if (auto.getCenaPoObnizce() < maxCena) {
                System.out.println("\n--- Samochód " + (i+1) + " ---");
                System.out.println(auto);
                znaleziono = true;
            }
        }

        if (!znaleziono) {
            System.out.println("Nie znaleziono samochodów o cenie poniżej podanej wartości.");
        }
    }


    private static void zapiszBazeDoPliku() {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("baza.bin"))) {
            oos.writeObject(baza);
            System.out.println("Baza danych została zapisana do pliku.");
        } catch (IOException e) {
            System.out.println("Błąd podczas zapisu pliku: " + e.getMessage());
        }
    }

    private static void symulujParking() {
        Parking parking = new Parking(baza);
        parking.symulujParking();
    }
}
