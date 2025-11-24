package Dostawa;

import java.io.Serializable;

public class DostawaKurier implements SposóbDostawy, Serializable {

    private String adres;
    private boolean ekspresowa;
    private boolean nadane;

    public DostawaKurier() {
        this.ekspresowa = false;
        this.nadane = false;
    }

    public String getAdres() {
        return adres;
    }

    public void setAdres(String adres) {
        this.adres = adres;
    }

    public boolean isEkspresowa() {
        return ekspresowa;
    }

    public void setEkspresowa(boolean ekspresowa) {
        this.ekspresowa = ekspresowa;
    }

    public DostawaKurier(String adres, boolean ekspresowa) {
        this();
        this.adres = adres;
    }

    public String toString() {
        return String.format("DostawaKurier adres: %s, Ekspresowa: %b", adres, ekspresowa);
    }

    public void potwierdźNadanie() {
        this.nadane = true;
    }
}
