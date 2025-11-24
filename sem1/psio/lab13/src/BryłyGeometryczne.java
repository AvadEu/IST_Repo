import java.util.*;

public class BryłyGeometryczne {

    private ArrayList<Bryła> baza;

    public BryłyGeometryczne() {
        baza = new ArrayList<>();
    }

    public ArrayList<Bryła> getBaza() {
        return baza;
    }

    public void addBryła(Bryła b) {
        baza.add(b);
    }

    public void wyświetlBaza() {
        for (Bryła b: baza) {
            System.out.println(b.toString());
        }
    }

    public Bryła getObiektZMaxObjętość() {
        double maxObj = -1;
        int pozycja = 0;
        for (Bryła current : baza) {
            if (current.Objętość() > maxObj) {
                maxObj = current.Objętość();
                pozycja = baza.indexOf(current);
            }
        }
        return baza.get(pozycja);
    }

    public void dodajBryły() {
        Random rand = new Random();
        Bryła p1 = new Prostopadłościan("Czerwony", 2, 2, rand.nextInt(1,10));
        Bryła p2 = new Prostopadłościan("Niebieski", 2, 2, rand.nextInt(1,10));
        Bryła w1 = new Walec("Zielony", 5, rand.nextInt(1, 10));
        Bryła w2 = new Walec("Niebieski", 5, rand.nextInt(1, 10));

        this.addBryła(p1);
        this.addBryła(p2);
        this.addBryła(w1);
        this.addBryła(w2);
    }

    public int pozycja(Bryła b) {
        return baza.indexOf(b);
    }

    public static void main(String[] args) {

        BryłyGeometryczne bryły = new BryłyGeometryczne();

        Scanner sc = new Scanner(System.in);

        while (true) {

            displayMenu();

            int choice = sc.nextInt();

            switch (choice) {
                case 1:
                    bryły.wyświetlBaza();
                    break;
                case 2:
                    Bryła b = utwórzBryłę();
                    bryły.addBryła(b);
                    System.out.printf("Pomyślnie dodano bryłę: %s%n", b.toString());
                    break;
                case 3:
                    bryły.dodajBryły();
                    System.out.println("Pomyślnie dodano bryły!");
                    break;
                case 4:
                    bryły.sortujPoKolorach();
                    break;
                case 5:
                    bryły.sortujPoWysokości();
                    break;
                case 6:
                    bryły.sortujPoKolorachWysokości();
                    break;
                case 7:
                    Bryła maxObj = bryły.getObiektZMaxObjętość();
                    System.out.printf("Bryła o największej objętości (%.2f) na pozycji %d:%n", maxObj.Objętość(), bryły.pozycja(maxObj));
                    break;
                case 8:
                    System.exit(0);
                default:
                    System.out.println("Nieprawidłowa opcja");
                    break;
            }
        }
    }

    public static void displayMenu() {
        System.out.println("1 - Wyświetl wszystkie bryły.");
        System.out.println("2 - Dodaj bryłę");
        System.out.println("3 - Dodaj bryły");
        System.out.println("4 - Sortuj bryły po kolorze");
        System.out.println("5 - Sortuj bryły po wysokości");
        System.out.println("6 - Sortuj bryły po kolorze i wysokości");
        System.out.println("7 - Wyświetl bryłę z największą objętością");
        System.out.println("8 - Zakończ program");
    }

    public static Bryła utwórzBryłę() {
        Scanner sc = new Scanner(System.in);

        System.out.println("Podaj kolor: ");
        String kolor = sc.nextLine();

        System.out.println("Podaj wysokość: ");
        int h = sc.nextInt();

        System.out.println("1 - Prostopadłościan");
        System.out.println("2 - Walec");

        int choice = sc.nextInt();
        switch (choice) {
            case 1:

                System.out.println("Podaj jeden bok prostopadłościanu:");
                int a = sc.nextInt();
                sc.nextLine();

                System.out.println("Podaj drugi bok prostopadłościanu:");
                int b = sc.nextInt();
                sc.nextLine();

                return new Prostopadłościan(kolor, h, a ,b);
            case 2:

                System.out.println("Podaj promień podstawy walca:");
                int r = sc.nextInt();
                sc.nextLine();

                return new Walec(kolor, h, r);
        }
        return null;
    }

    // Komparator do porównywania według koloru
    public class BryłaKolorComparator implements Comparator<Bryła> {
        @Override
        public int compare(Bryła b1, Bryła b2) {
            return b1.getKolor().compareTo(b2.getKolor());
        }
    }

    // Komparator do porównywania według wysokości
    public class BryłaWysokośćComparator implements Comparator<Bryła> {
        @Override
        public int compare(Bryła b1, Bryła b2) {
            return Integer.compare(b1.getH(), b2.getH());
        }
    }

    // Komparator do porównywania według koloru i wysokości
    public class BryłaKolorWysokośćComparator implements Comparator<Bryła> {
        @Override
        public int compare(Bryła b1, Bryła b2) {
            int result = b1.getKolor().compareTo(b2.getKolor());
            if (result == 0) {
                return Integer.compare(b1.getH(), b2.getH());
            }
            return result;
        }
    }

    public void sortujPoKolorach() {
        Collections.sort(baza, new BryłaKolorComparator());
        System.out.println("\nPosortowane według koloru:");
        for (Bryła b : baza) {
            System.out.println(b.toString());
        }
    }

    public void sortujPoWysokości() {
        Collections.sort(baza, new BryłaWysokośćComparator());
        System.out.println("\nPosortowane według wysokości:");
        for (Bryła b : baza) {
            System.out.println(b.toString());
        }
    }

    public void sortujPoKolorachWysokości() {
        Collections.sort(baza, new BryłaKolorWysokośćComparator());
        System.out.println("\nPosortowane według koloru i wysokości:");
        for (Bryła b : baza) {
            System.out.println(b.toString());
        }
    }

}