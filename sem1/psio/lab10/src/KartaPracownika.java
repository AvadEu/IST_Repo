public abstract class KartaPracownika {
    private int numer;
    private String nazwisko;

    public KartaPracownika() {
        this.numer = 0;
        this.nazwisko = null;
    }

    public KartaPracownika(int numer, String nazwisko){
        this.numer = numer;
        this.nazwisko = nazwisko;
    }

    public String toString() {
        return this.numer + " " + this.nazwisko;
    }

    abstract public double premia();
}
