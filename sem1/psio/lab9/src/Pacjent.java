public class Pacjent extends Osoba{
    private int n;
    private Wizyta[] wizyty;
    private int umowione;

    public Pacjent(){
        super();
        this.n = 0;
        this.wizyty = null;
        this.umowione = 0;
    }

    public Pacjent(String nazwisko, String pesel, int n) {
        super(nazwisko, pesel);
        this.n = n;
        this.wizyty = new Wizyta[n];
    }

    public double Oblicz() {
        int sum = 0;
        for (int i = 0; i < this.n; i++) {
            sum += this.wizyty[i].getCenaWizyty();
        }
        return sum;
    }

    public String toString() {
        return String.format("Pacjent: %s [n=%d]", super.toString(), this.n);
    }

    public void wyświetlWizyty() {
        if (this.wizyty != null) {
            for (Wizyta w: this.wizyty) {
                System.out.println(w.toString());
            }
        } else {
            System.out.println("Brak wizyt!");
        }
    }

    public void addWizyta(Wizyta wizyta) {
        if (this.wizyty == null) {
            this.wizyty = new Wizyta[n];
        }
        this.wizyty[umowione] = wizyta;
        this.umowione++;
    }
}
