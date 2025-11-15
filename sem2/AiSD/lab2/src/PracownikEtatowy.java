public class PracownikEtatowy extends Pracownik {

    private double etat;
    private double pensja;

    public PracownikEtatowy() {
        super();
        this.etat = 1.0;
        this.pensja = 3500;
    }

    public PracownikEtatowy(String imię, String nazwisko, String stanowisko, long pesel, int staz, double etat, double stawka) {
        super(nazwisko, imię, pesel, stanowisko, staz);
        this.etat = etat;
        this.pensja = stawka;
    }

    public double pensja() {
        return etat * pensja;
    }

    public double getEtat() {
        return etat;
    }

    public void setEtat(double etat) {
        this.etat = etat;
    }

    public double getPensja() {
        return pensja;
    }

    public void setPensja(double pensja) {
        this.pensja = pensja;
    }

    @Override
    public String toString() {
        return super.toString();
    }
}