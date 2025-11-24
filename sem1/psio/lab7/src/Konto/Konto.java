package Konto;

import Osoba.Osoba;

public class Konto {
    private Waluta waluta;
    private boolean jestAktywne;

    public Konto() {
        this.jestAktywne = false;
    }

    public Konto(Waluta waluta) {
        this();
        this.waluta = waluta;
    }

    public Waluta getWaluta() {
        return waluta;
    }

    public void setWaluta(Waluta waluta) {
        this.waluta = waluta;
    }

    public boolean getJestAktywne() {
        return jestAktywne;
    }

    public void setJestAktywne(boolean jestAktywne) {
        this.jestAktywne = jestAktywne;
    }

    public void aktywuj() {
        Osoba.aktywujKonto(this);
    }

    public void dezaktywuj() {
        Osoba.dezaktywujKonto(this);
    }

    public void getStan() {
        System.out.printf("waluta=%s jestAktywne=%b%n", this.getWaluta().getStan(), this.getJestAktywne());
    }
}
