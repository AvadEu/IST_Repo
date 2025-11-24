public class Przychodnia {
    private static Osoba[] osoby = new Osoba[20];
    private static int n;

    public static void main(String[] args) {

        // Wstawianie lekarzy
        osoby[0] = new Lekarz();
        osoby[1] = new Lekarz("Kowalski", "69052056537", "Internista", 250);
        osoby[2] = new Lekarz("Nowak", "52090871617", "Neurochirurg", 300);
        n += 3;

        System.out.println();

        // Wstawianie pacjentów
        osoby[3] = new Pacjent();
        osoby[4] = new Pacjent("Wiśniewski", "99041889211", 1);
        osoby[5] = new Pacjent("Lewandowski", "99021833317", 2);
        n += 3;

        // Dodanie wizyt
        Wizyta w = new Wizyta();
        Wizyta w2 = new Wizyta(1, 250, false, true);
        Wizyta w3 = new Wizyta(5, 150, true, true);

//        ((Pacjent)osoby[3]).addWizyta(w);
        ((Pacjent)osoby[4]).addWizyta(w2);
        ((Pacjent)osoby[5]).addWizyta(w2);
        ((Pacjent)osoby[5]).addWizyta(w3);

        System.out.println();

        // Wyświetlanie wszystkich osób
        for (int i = 0; i < n; i++) {
            System.out.println(osoby[i].toString());
        }

        System.out.println();

        // Wyświetlanie samych lekarzy
        for (int i = 0; i < n; i++) {
            if (osoby[i] instanceof Lekarz) {
                System.out.println(osoby[i].toString());
                ((Lekarz) osoby[i]).wyświetlLiczęPacjentów();
            }
        }

        System.out.println();

        // Wyświetlanie samych pacjentów
        for (int i = 0; i < n; i++) {
            if (osoby[i] instanceof Pacjent) {
                System.out.println(osoby[i].toString());
                ((Pacjent) osoby[i]).wyświetlWizyty();
            }
            System.out.println();
        }

        System.out.println();

        // Liczenie internistów
        int liczbaInternistów = 0;
        for (int i = 0; i < n; i++) {
            if (osoby[i] instanceof Lekarz && ((Lekarz) osoby[i]).jestInternista()) {
                liczbaInternistów++;
            }
        }
        System.out.println("W przychodni pracuje " + liczbaInternistów + " internistów!");

        System.out.println();

        // Obliczanie zarobków lekarzy
        double max_zarobek = -1;
        Lekarz max_lekarz = new Lekarz();
        for (int i = 0; i < n; i++) {
            if (osoby[i] instanceof Lekarz) {
                double zarobek = ((Lekarz)osoby[i]).Oblicz();
                if (max_zarobek < zarobek) {
                    max_zarobek = zarobek;
                    max_lekarz = (Lekarz) osoby[i];
                }
            }
        }
        System.out.printf("Najwięcej (%.2fPLN) zarobił: %n%s", max_zarobek, max_lekarz.toString());
    }
}
