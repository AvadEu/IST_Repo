public class Main {
    public static void main(String[] args) {

        final int n = 5;
        Samolot[] lotnisko = new Samolot[n];

        lotnisko[0] = new SamolotTowarowy("Airbus", "500S", 10000, 7000);
        lotnisko[1] = new SamolotTowarowy("Airbus", "200S", 5000, 5000);

        lotnisko[2] = new SamolotOsobowy("Boeing", "737", 2);
        lotnisko[3] = new SamolotOsobowy("Boeing", "787", 3);
        lotnisko[4] = new SamolotOsobowy("Boeing", "900", 4);

        ((SamolotOsobowy) lotnisko[2]).dodajPasażera(new Pasażer("Michał", "Nowak", 70));
        ((SamolotOsobowy) lotnisko[2]).dodajPasażera(new Pasażer("Jan", "Jakis", 75));

        ((SamolotOsobowy) lotnisko[3]).dodajPasażera(new Pasażer("Jacek", "Miły", 80));
        ((SamolotOsobowy) lotnisko[3]).dodajPasażera(new Pasażer("Adam", "Śmieszny", 85));
        ((SamolotOsobowy) lotnisko[3]).dodajPasażera(new Pasażer("Miłosz", "Pomocny", 89));

        ((SamolotOsobowy) lotnisko[4]).dodajPasażera(new Pasażer("Kamil", "Makowski", 73));
        ((SamolotOsobowy) lotnisko[4]).dodajPasażera(new Pasażer("Karol", "Wiśniewski", 74));
        ((SamolotOsobowy) lotnisko[4]).dodajPasażera(new Pasażer("Kuba", "Kowalski", 75));
        ((SamolotOsobowy) lotnisko[4]).dodajPasażera(new Pasażer("Konrad", "Nowakowski", 76));


        for (int i = 0; i < lotnisko.length; i++) {
            if (lotnisko[i] != null) {
                lotnisko[i].getStan();
            }
        }
    }
}