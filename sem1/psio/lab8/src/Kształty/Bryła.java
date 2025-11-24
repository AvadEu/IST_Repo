package Kształty;

public abstract class Bryła {
    private String nazwa;
    private int h;

    public Bryła() {
        this.nazwa = "";
        this.h = 0;
    }

    public Bryła(String nazwa, int h) {
        this.nazwa = nazwa;
        this.h = h;
    }

    public String toString() {
        return "Bryła o nazwie: " + nazwa;
    }

    public abstract double Objętość();

    public abstract double Pole();

    public String getNazwa() {
        return nazwa;
    }

    public void setNazwa(String nazwa) {
        this.nazwa = nazwa;
    }

    public int getH() {
        return h;
    }

    public void setH(int h) {
        this.h = h;
    }
}
