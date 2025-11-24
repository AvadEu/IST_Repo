package Kształty;

public class Prostopadłościan extends Bryła{
    private int a; // Bok podstawy
    private int b; // Bok podstawy

    public Prostopadłościan() {
        super("Bazowy", 1);
        this.a = 1;
        this.b = 1;
    }

    public Prostopadłościan(String nazwa, int h, int a, int b) {
        super(nazwa, h);
        this.a = a;
        this.b = b;
    }

    public double Objętość() {
        return this.a * this.b + super.getH();
    }

    public double Pole() {
        return 2 * (this.a * this.b + this.a * super.getH() + this.b * super.getH());
    }

    public String toString() {
        return String.format("Prostopadłościan: %s [a=%2d, b=%2d, h=%2d]", this.getNazwa(), this.a, this.b, this.getH());
    }

    public boolean jestSześcianem() {
        if (a == b && b == super.getH()) {
            return true;
        } else {
            return false;
        }
    }
}
