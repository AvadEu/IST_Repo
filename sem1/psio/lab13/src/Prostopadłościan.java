public class Prostopadłościan extends Bryła{

    private int a;
    private int b;
    private boolean jestSześcianem;

    public Prostopadłościan(String kolor, int h, int a, int b) {
        super(kolor, h);
        this.a = a;
        this.b = b;
        this.jestSześcianem = czySześcian(a, b, super.getH());
    }

    public Prostopadłościan() {
        super();
        this.a = 1;
        this.b = 1;
        this.jestSześcianem = true;
    }

    public int getA() {
        return a;
    }

    public void setA(int a) {
        this.a = a;
    }

    public int getB() {
        return b;
    }

    public void setB(int b) {
        this.b = b;
    }

    public boolean isJestSześcianem() {
        return jestSześcianem;
    }

    public void setJestSześcianem(boolean jestSześcianem) {
        this.jestSześcianem = jestSześcianem;
    }

    private boolean czySześcian(int a, int b, int h) {
        return a == b && a == h;
    }

    public double Objętość() {
        return a * b * super.getH();
    }

    @Override
    public String toString() {
        return String.format("Prostopadłościan: [\"%s\", a=%d, b=%d, h=%d]",super.getKolor(), a, b, super.getH());
    }
}
