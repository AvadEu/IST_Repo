package Dostawa;

public class DostawaOdbiór implements SposóbDostawy {

    private String Adres;
    private int waga;
    private boolean nadane;

    public DostawaOdbiór() {
        this.nadane = false;
    }

    public DostawaOdbiór(String adres, int waga) {
        this();
        this.Adres = adres;
        this.waga = waga;
    }

    public void potwierdźNadanie() {
        this.nadane = true;
    }

    public String getAdres() {
        return Adres;
    }

    public void setAdres(String adres) {
        Adres = adres;
    }

    public int getWaga() {
        return waga;
    }

    public void setWaga(int waga) {
        this.waga = waga;
    }

    public String toString() {
        return String.format("Adres: %s, waga: %dkg", Adres, waga);
    }
}
