public class Main {
    public static void main(String[] args) {
        Car a1 = new Car();
        Car a2 = new Car();

        final int liczba_aut = 3;

        Car [] samochody = new Car(3);
        a2.setSilnik(null);

        Mechanik.podbijPrzegląd(a1);
        Mechanik.podbijPrzegląd(a2);

        a1.getStan();
        System.out.println();
        a2.getStan();
    }
}