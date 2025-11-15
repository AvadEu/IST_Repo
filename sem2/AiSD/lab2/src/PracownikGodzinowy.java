public class PracownikGodzinowy extends Pracownik {

    private double stawka;
    private int liczba_godz;

    public PracownikGodzinowy() {
        super();
        this.stawka = 35;
        this.liczba_godz = 160;
    }

    public PracownikGodzinowy(String imię, String nazwisko, String stanowisko, long pesel, int staz, double stawka, int liczba_godz) {
        super(nazwisko, imię, pesel, stanowisko, staz);
        this.stawka = stawka;
        this.liczba_godz = liczba_godz;
    }

    @Override
    public String toString() {
        return super.toString();
    }

    public double getStawka() {
        return stawka;
    }

    public void setStawka(double stawka) {
        this.stawka = stawka;
    }

    public int getLiczba_godz() {
        return liczba_godz;
    }

    public void setLiczba_godz(int liczba_godz) {
        this.liczba_godz = liczba_godz;
    }

    public double pensja() {
        return stawka * liczba_godz;
    }
}
