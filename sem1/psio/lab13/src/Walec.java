public class Walec extends Bryła{

    private int r;

    public Walec() {
        super();
        this.r = 1;
    }

    public Walec(String kolor, int h, int r) {
        super(kolor, h);
        this.r = r;
    }

    public int getR() {
        return r;
    }

    public void setR(int r) {
        this.r = r;
    }

    public double Objętość() {
        return Math.PI * Math.pow(r, 2) * super.getH();
    }

    @Override
    public String toString() {
        return String.format("Walec: [\"%s\", r=%d, h=%d]",super.getKolor(), r, super.getH());
    }
}
