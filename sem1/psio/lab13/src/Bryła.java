abstract public class Bryła {

    private String kolor;
    private int h;

    public Bryła() {
        this.kolor = "";
        this.h = 1;
    }

    public Bryła(String kolor, int h) {
        this.kolor = kolor;
        this.h = h;
    }

    public String getKolor() {
        return kolor;
    }

    public void setKolor(String kolor) {
        this.kolor = kolor;
    }

    public int getH() {
        return h;
    }

    public void setH(int h) {
        this.h = h;
    }

    public abstract double Objętość();
}
