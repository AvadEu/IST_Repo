package Kształty;

public class Walec extends Bryła {
    private int r;

    public Walec() {
        super("Bazowy", 1);
        this.r = 1;
    }

    public Walec(String nazwa, int h, int r) {
        super(nazwa, h);
        this.r = r;
    }

    public double Objętość() {
        return Math.PI * super.getH() * r * r;
    }

    public double Pole() {
        return 2 * Math.PI * r * r;
    }

    public String toString() {
        return String.format("Walec: %s [r=%2d, h=%2d]", this.getNazwa(), this.r, this.getH());
    }

    public boolean obrótKwadratu() {
        if (this.getH() == 2 * this.r) {
            return true;
        } else {
            return false;
        }
    }
}
