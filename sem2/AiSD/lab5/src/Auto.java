import java.io.Serializable;

public class Auto implements Serializable {
    private int nrSilnika;
    private String marka;
    private String typ;
    private String dataProdukcji;
    private double cena;
    private String kolor;
    private int skladowanie;
    private double przecena;

    public Auto(int nrSilnika, String marka, String typ, String dataProdukcji,
                double cena, String kolor, int skladowanie) {
        this.nrSilnika = nrSilnika;
        this.marka = marka;
        this.typ = typ;
        this.dataProdukcji = dataProdukcji;
        this.cena = cena;
        this.kolor = kolor;
        this.skladowanie = skladowanie;
        obliczPrzecene();
    }

    private void obliczPrzecene() {
        if (skladowanie >= 15) {
            przecena = cena * 0.15;
        } else if (skladowanie >= 6) {
            przecena = cena * 0.06;
        } else {
            przecena = 0;
        }
    }

    public double getCenaPoObnizce() {
        return cena - przecena;
    }

    public int getNrSilnika() {
        return nrSilnika;
    }

    public String getMarka() {
        return marka;
    }

    public double getCena() {
        return cena;
    }

    public int getSkladowanie() {
        return skladowanie;
    }

    public void setSkladowanie(int skladowanie) {
        this.skladowanie = skladowanie;
        obliczPrzecene();
    }

    public void setCena(int cena) {
        this.cena = cena;
        obliczPrzecene();
    }

    public void setKolor(String kolor) {
        this.kolor = kolor;
        obliczPrzecene();
    }

    @Override
    public String toString() {
        return "Nr silnika: " + nrSilnika +
                "\nMarka: " + marka +
                "\nTyp: " + typ +
                "\nData produkcji: " + dataProdukcji +
                "\nCena: " + cena +
                "\nKolor: " + kolor +
                "\nSkładowanie (miesiące): " + skladowanie +
                "\nPrzecena: " + przecena +
                "\nCena po obniżce: " + getCenaPoObnizce();
    }
}
