import java.util.Objects;

public class Karta {
    private int wartosc;
    private int kolor;

    public Karta(int wartosc, int kolor) {
        this.wartosc = wartosc;
        this.kolor = kolor;
    }

    public int getWartosc() {
        return wartosc;
    }

    public void setWartosc(int wartosc) {
        this.wartosc = wartosc;
    }

    public int getKolor() {
        return kolor;
    }

    public void setKolor(int kolor) {
        this.kolor = kolor;
    }

    @Override
    public String toString() {
        String[] values = {"0", "As", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Walet", "Dama", "Król"};
        String[] colors = {"Kier", "Karo", "Trefl", "Pik"};
        return values[wartosc] + " - " + colors[kolor];
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || this.getClass() != obj.getClass()) return false;
        Karta k = (Karta) obj;
        return this.wartosc == k.wartosc && this.kolor == k.kolor;
    }

    @Override
    public int hashCode() {
        return Objects.hash(wartosc, kolor);
    }
}
