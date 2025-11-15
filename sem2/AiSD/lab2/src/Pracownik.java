import java.io.Serializable;

public abstract class Pracownik implements Serializable {
    private String nazwisko;
    private String imię;
    private long pesel;
    private String stanowisko;
    private int staż;

    public Pracownik() {
        nazwisko = "";
        imię = "";
        pesel = 0;
        stanowisko = "";
        staż = 0;
    }

    public Pracownik(String nazwisko, String imie, long pesel, String stanowisko, int staz) {
        this.nazwisko = nazwisko;
        this.imię = imie;
        this.pesel = pesel;
        this.stanowisko = stanowisko;
        this.staż = staz;
    }

    public void wyświetl() {
        System.out.printf("| %-15s | %-10s | %-12d | %-15s | %10d | %8.2f   |\n",
                nazwisko, imię, pesel, stanowisko, staż, pensja());
    }

    @Override
    public String toString() {
        return String.format("%s %s %d %s %d %.2f",
                nazwisko, imię, pesel, stanowisko, staż, pensja());
    }

    public abstract double pensja();

    public String getNazwisko() {
        return nazwisko;
    }

    public void setNazwisko(String nazwisko) {
        this.nazwisko = nazwisko;
    }

    public String getImię() {
        return imię;
    }

    public void setImię(String imię) {
        this.imię = imię;
    }

    public long getPesel() {
        return pesel;
    }

    public void setPesel(long pesel) {
        this.pesel = pesel;
    }

    public String getStanowisko() {
        return stanowisko;
    }

    public void setStanowisko(String stanowisko) {
        this.stanowisko = stanowisko;
    }

    public int getStaż() {
        return staż;
    }

    public void setStaż(int staż) {
        this.staż = staż;
    }
}
