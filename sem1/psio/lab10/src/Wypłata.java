import java.util.Enumeration;

public class Wypłata {
    private static int counter = 0;
    private int numerWypłaty;
    private double pensja;
    private KartaPracownika karta;

    public Wypłata() {
        this.numerWypłaty = ++counter;
        this.pensja = 0;
    }

    public Wypłata(double pensja, KartaPracownika karta) {
        this();
        this.pensja = pensja;
        this.karta = karta;
    }

    public String toString() {
        return "Wypłata " + numerWypłaty + " [Pensja: " + this.pensja + " " + this.karta.getClass().getName() + ": " + this.karta.toString() + "]";
    }

    public double pensjaZPremia() {
        return this.pensja * (1 + this.karta.premia());
    }

    public void setKarta(KartaPracownika karta) {
        this.karta = karta;
    }

    public KartaPracownika getKarta() {
        return this.karta;
    }
}
