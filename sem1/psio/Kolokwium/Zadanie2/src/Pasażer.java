public class Pasażer {
    private String imie;
    private String nazwisko;
    private int waga;

    public Pasażer(String imie, String nazwisko, int waga) {
        this.imie = imie;
        this.nazwisko = nazwisko;
        this.waga = waga;
    }

    public String toString() {
        return this.imie + " " + this.nazwisko + " " + this.waga + "kg";
    }

    public void getStan() {
        System.out.println(this.toString());
    }
}
