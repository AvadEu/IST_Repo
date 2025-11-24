public class Silnik {
    private int moc;
    private String typ;
    private double pojemność;
    private boolean czyDoładowany;

    public Silnik() {
        this.moc = 100;
        this.typ = "rzędowy";
        this.pojemność = 1.6;
        this.czyDoładowany = false;
    }

    public Silnik(int moc, String typ, double pojemnosc, boolean czyDoładowany) {
        this.moc = moc;
        this.typ = typ;
        this.pojemność = pojemnosc;
        this.czyDoładowany = czyDoładowany;
    }

    public int getMoc() {
        return moc;
    }

    public void setMoc(int moc) {
        this.moc = moc;
    }

    public String getTyp() {
        return typ;
    }

    public void setTyp(String typ) {
        this.typ = typ;
    }

    public double getPojemność() {
        return pojemność;
    }

    public void setPojemność(double pojemność) {
        this.pojemność = pojemność;
    }

    public boolean isCzyDoładowany() {
        return czyDoładowany;
    }

    public void setCzyDoładowany(boolean czyDoładowany) {
        this.czyDoładowany = czyDoładowany;
    }

    public void getStan() {
        System.out.println("moc: " + moc);
        System.out.println("typ: " + typ);
        System.out.println("pojemność: " + pojemność);
        System.out.println("czyDoładowany:" + czyDoładowany);
    }
}
