import java.util.ArrayList;
import java.util.InputMismatchException;
import java.util.Scanner;

public class Main {

    private static Magazyn magazyn = null;
    private static ArrayList<Klient> listaKlientow = new ArrayList<>();
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        int wybor;

        do {
            wyswietlMenu();
            wybor = pobierzWyborUzytkownika();

            switch (wybor) {
                case 1:
                    utworzMagazyn();
                    break;
                case 2:
                    utworzKlienta();
                    break;
                case 3:
                    dodajZamowienieDoKlienta();
                    break;
                case 4:
                    zglosKlientaDoMagazynu();
                    break;
                case 5:
                    realizujZamowienia();
                    break;
                case 6:
                    obliczPrzychodyFirmy();
                    break;
                case 0:
                    System.exit(0);
                    break;
                default:
                    System.out.println("Nieprawidłowy wybór. Spróbuj ponownie.");
            }
            System.out.println();

        } while (wybor != 0);

        scanner.close();
    }

    private static void wyswietlMenu() {
        System.out.println("======== MENU ========");
        System.out.println("1. Utwórz nowy magazyn");
        System.out.println("2. Utwórz nowego klienta");
        System.out.println("3. Dodaj zamówienie do klienta");
        System.out.println("4. Zgłoś klienta do magazynu");
        System.out.println("5. Zrealizuj zamówienia w magazynie");
        System.out.println("6. Skonstruuj firmę i oblicz jej przychody");
        System.out.println("0. Wyjście");
        System.out.print("Wybierz opcję: ");
    }

    private static int pobierzWyborUzytkownika() {
        int wybor = -1;
        try {
            wybor = scanner.nextInt();
        } catch (InputMismatchException e) {
            System.out.println("Błąd: Wprowadź liczbę całkowitą.");
        } finally {
            scanner.nextLine();
        }
        return wybor;
    }

    private static void utworzMagazyn() {
        magazyn = new Magazyn();
        System.out.println("Nowy magazyn został utworzony.");
    }


    private static void utworzKlienta() {
        System.out.println("\n--- Tworzenie Klienta ---");
        System.out.print("Podaj nazwę nowego klienta: ");
        String nazwa = scanner.nextLine();

        if (nazwa.trim().isEmpty()) {
            System.out.println("Błąd: Nazwa klienta nie może być pusta.");
            return;
        }

        boolean istnieje = false;
        for (Klient k : listaKlientow) {
            if (k.getNazwa().equalsIgnoreCase(nazwa)) {
                istnieje = true;
                break;
            }
        }

        if (istnieje) {
            System.out.println("Klient o nazwie '" + nazwa + "' już istnieje.");
        } else {
            Klient nowyKlient = new Klient(nazwa);
            listaKlientow.add(nowyKlient);
            System.out.println("Utworzono klienta: " + nazwa);
        }
    }

    private static Klient znajdzKlienta(String nazwa) {
        for (Klient k : listaKlientow) {
            if (k.getNazwa().equalsIgnoreCase(nazwa)) {
                return k;
            }
        }
        return null;
    }


    private static void dodajZamowienieDoKlienta() {
        System.out.println("\n--- Dodawanie Zamówienia ---");
        if (listaKlientow.isEmpty()) {
            System.out.println("Brak klientów. Utwórz najpierw klienta (opcja 2).");
            return;
        }

        System.out.print("Podaj nazwę klienta, do którego chcesz dodać zamówienie: ");
        String nazwaKlienta = scanner.nextLine();

        Klient klient = znajdzKlienta(nazwaKlienta);

        if (klient == null) {
            System.out.println("Nie znaleziono klienta o nazwie: " + nazwaKlienta);
            return;
        }

        try {
            System.out.print("Podaj nazwę towaru: ");
            String towar = scanner.nextLine();
            if (towar.trim().isEmpty()) {
                System.out.println("Błąd: Nazwa towaru nie może być pusta.");
                return;
            }


            System.out.print("Podaj liczbę sztuk: ");
            int sztuk = scanner.nextInt();
            scanner.nextLine();

            if(sztuk <= 0) {
                System.out.println("Błąd: Liczba sztuk musi być dodatnia.");
                return;
            }

            System.out.print("Podaj cenę jednostkową: ");
            double cena = scanner.nextDouble();
            scanner.nextLine();

            if(cena <= 0) {
                System.out.println("Błąd: Cena musi być dodatnia.");
                return;
            }

            Zamowienie zamowienie = new Zamowienie(towar, sztuk, cena);
            klient.dodajZamowienie(zamowienie);

        } catch (InputMismatchException e) {
            System.out.println("Błąd: Wprowadzono nieprawidłowe dane liczbowe (liczba sztuk lub cena).");
            scanner.nextLine();
        }
    }

    private static void zglosKlientaDoMagazynu() {
        System.out.println("\n--- Zgłaszanie Klienta do Magazynu ---");
        if (magazyn == null) {
            System.out.println("Brak magazynu. Utwórz najpierw magazyn (opcja 1).");
            return;
        }
        if (listaKlientow.isEmpty()) {
            System.out.println("Brak klientów do zgłoszenia. Utwórz najpierw klienta (opcja 2).");
            return;
        }

        System.out.print("Podaj nazwę klienta do zgłoszenia: ");
        String nazwaKlienta = scanner.nextLine();

        Klient klient = znajdzKlienta(nazwaKlienta);

        if (klient == null) {
            System.out.println("Nie znaleziono klienta o nazwie: " + nazwaKlienta);
            return;
        }

        ZgloszenieKlienta zgloszenie = klient.stworzZgloszenie();
        magazyn.dodajZgloszenie(zgloszenie);
    }


    private static void realizujZamowienia() {
        System.out.println("\n--- Realizacja Zamówień w Magazynie ---");
        if (magazyn == null) {
            System.out.println("Brak magazynu. Utwórz najpierw magazyn (opcja 1).");
            return;
        }

        magazyn.przetworzZgloszenia();
    }

    private static void obliczPrzychodyFirmy() {
        Magazyn m1 = new Magazyn();
        Magazyn m2 = new Magazyn();

        Zamowienie z1 = new Zamowienie("Ananas", 10, 10.5);
        Zamowienie z2 = new Zamowienie("Kawa", 10, 15);

        Klient k1 = new Klient("Jan");
        Klient k2 = new Klient("Kamil");

        k1.dodajZamowienie(z1);
        k2.dodajZamowienie(z2);

        m1.dodajZgloszenie(k1.stworzZgloszenie());
        m2.dodajZgloszenie(k2.stworzZgloszenie());

        Firma f = new Firma();

        f.dodajMagazyn(m1);
        f.dodajMagazyn(m2);

        System.out.println("Przychody firmy: " + f.getPrzychodyFirmy());
    }
}
