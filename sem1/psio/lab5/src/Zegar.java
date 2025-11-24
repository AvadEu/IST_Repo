public class Zegar {

    private int czas;

    public Zegar() {
        this.czas = 0;
    }

    public Zegar(int hh, int mm, int ss) {
        this.czas = (3600 * hh + 60 * mm + ss) % (24 * 3600);
    }

    public void Przesun(int hh, int mm, int ss) {
        this.czas += 3600 * hh + 60 * mm + ss;
        this.czas = this.czas % (24 * 3600);
    }

    public void Wypisz() {
        System.out.println("Liczba sekund od północy: " + this.czas);
        int hh = this.czas / 3600;
        int mm = this.czas % 3600 / 60;
        int ss = this.czas % 3600 % 60;
        System.out.printf("%d:%d:%d%n", hh, mm, ss);
    }
}
