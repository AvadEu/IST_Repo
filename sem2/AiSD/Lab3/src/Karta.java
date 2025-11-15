public class Karta implements Comparable<Karta> {
    private int wartosc;
    private int kolor;
    private boolean odkryta;

    public Karta(int wartosc, int kolor, boolean znacznik) {
        this.wartosc = wartosc;
        this.kolor = kolor;
        this.odkryta = znacznik;
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

    public boolean isOdkryta() {
        return odkryta;
    }

    @Override
    public String toString() {
        String[] values = {"0", "As", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Walet", "Dama", "Król"};
        String[] colors = {"Kier", "Karo", "Trefl", "Pik"};
        if (isOdkryta()) {
            return values[wartosc] + " - " + colors[kolor];
        } else {
            return "() - Karta Zakryta!";
        }
    }

    @Override
    public int compareTo(Karta o) {
        if (this.wartosc != o.wartosc) {
            return Integer.compare(this.wartosc, o.wartosc);
        }
        return Integer.compare(this.kolor, o.kolor);
    }
}
