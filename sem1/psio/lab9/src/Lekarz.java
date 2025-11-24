import java.util.Random;

public class Lekarz extends Osoba{
    private String s;
    private int stawka;
    private int[] t;

    public Lekarz() {
        super();
        this.s = "";
        this.stawka = 0;
        this.t = null;
    }

    public Lekarz(String nazwisko, String pesel, String spec, int stawka) {
        super(nazwisko, pesel);
        this.s = spec;
        this.stawka = stawka;
        this.t = randomHoursArray(5);

    }

    @Override
    public double Oblicz() {
        if (this.t == null) {
            return 0.0;
        } else {
            int sum = 0;
            for (int l: this.t) {
                sum += l;
            }
            return this.stawka * sum;
        }
    }

    public String toString() {
        return String.format("Lekarz: %5s [specjalizacja=%s, stawka=%s]", super.toString(), this.s, this.stawka);
    }

    public void wyświetlLiczęPacjentów() {
        if (this.t != null) {
            String[] days = {"Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"};

            System.out.println("Liczba pacjentów:");
            for (int i = 0; i < days.length; i++) {
                System.out.print(days[i] + ": " + this.t[i] + " ");
            }
            System.out.println();
        } else {
            System.out.println("Brak pacjentów!");
        }
    }

    public boolean jestInternista() {
        return this.s.equalsIgnoreCase("internista");
    }

    private int[] randomHoursArray(int n) {
        Random rand = new Random();

        int[] t = new int[n];
        for (int i = 0; i < n; i++) {
            t[i] = rand.nextInt(10, 31);
        }

        return t;
    }
}
