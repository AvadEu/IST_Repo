import java.util.Scanner;

public class Parking {
    private ListStack<Auto> parking;
    private Scanner scanner;

    public Parking(L2KCzS<Auto> baza) {
        parking = new ListStack<>();
        scanner = new Scanner(System.in);

        for (int i = 0; i < baza.size(); i++) {
            parking.push(baza.get(i));
        }
    }

    public void symulujParking() {
        if (parking.isEmpty()) {
            System.out.println("Brak samochodów na parkingu.");
            return;
        }

        System.out.println("\n=== Symulacja parkingu ===");
        System.out.println("Samochody są zaparkowane jeden za drugim.");

        while (true) {
            wyswietlSamochodyNaParkingu();

            System.out.println("\nCo chcesz zrobić?");
            System.out.println("1. Sprzedaj samochód");
            System.out.println("0. Zakończ symulację");

            int wybor = scanner.nextInt();
            scanner.nextLine();

            if (wybor == 0) {
                break;
            } else if (wybor == 1) {
                sprzedajSamochod();
            } else {
                System.out.println("Nieprawidłowy wybór.");
            }
        }
    }

    private void wyswietlSamochodyNaParkingu() {
        System.out.println("\nSamochody na parkingu:");

        ListStack<Auto> tempStack = new ListStack<>();
        Auto[] autos = new Auto[parking.size()];
        int count = 0;

        while (!parking.isEmpty()) {
            Auto auto = parking.pop();
            tempStack.push(auto);
            autos[count++] = auto;
        }

        while (!tempStack.isEmpty()) {
            parking.push(tempStack.pop());
        }

        for (int i = count - 1; i >= 0; i--) {
            Auto auto = autos[i];
            System.out.println((count - i) + ". Nr silnika: " + auto.getNrSilnika() +
                    ", Marka: " + auto.getMarka() +
                    ", Cena: " + auto.getCenaPoObnizce());
        }
    }

    private void sprzedajSamochod() {
        System.out.print("Podaj numer silnika samochodu do sprzedaży: ");
        int nrSilnika = scanner.nextInt();
        scanner.nextLine();

        ListStack<Auto> tempStack = new ListStack<>();

        if (!czyJestNaParkingu(nrSilnika)) {
            System.out.println("Brak na parkingu samochodu o podanym numerze silnika.");
            return;
        }

        boolean znaleziono = false;

        while (!parking.isEmpty() && !znaleziono) {
            Auto auto = parking.pop();

            if (auto.getNrSilnika() == nrSilnika) {
                znaleziono = true;
                System.out.println("Sprzedano samochód: " + auto.getMarka() +
                        " (Nr silnika: " + auto.getNrSilnika() + ")");
            } else {
                tempStack.push(auto);
                System.out.println("Samochód musi wyjechać: " + auto.getMarka() +
                        " (Nr silnika: " + auto.getNrSilnika() + ")");
            }
        }

        while (!tempStack.isEmpty()) {
            Auto auto = tempStack.pop();
            parking.push(auto);
            System.out.println("Samochód wraca na parking: " + auto.getMarka() +
                    " (Nr silnika: " + auto.getNrSilnika() + ")");
        }
    }

    public boolean czyJestNaParkingu(int nrSilnika) {
        if (parking.isEmpty()) {
            return false;
        }

        ListStack<Auto> tempStack = new ListStack<>();
        boolean znaleziono = false;

        while (!parking.isEmpty()) {
            Auto auto = parking.pop();
            tempStack.push(auto);

            if (auto.getNrSilnika() == nrSilnika) {
                znaleziono = true;
            }
        }

        while (!tempStack.isEmpty()) {
            parking.push(tempStack.pop());
        }

        return znaleziono;
    }

}
