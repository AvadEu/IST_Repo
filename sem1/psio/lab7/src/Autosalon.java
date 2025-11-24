import java.util.Random;

public class Autosalon {
    private int n;
    private Auto[] a;

    public Autosalon() {
        this.n = 0;
        this.a = null;
    }

    public Autosalon(int n) {
        this.n = n;
        this.a = new Auto[n];

        Random rand = new Random();

        for (int i = 0; i < n; i++) {
            int marka = rand.nextInt(50) + 1;
            int cena = rand.nextInt(5001);
            this.a[i] = new Auto(marka, cena);
        }
    }

    public void getAuta() {
        for (int i = 0; i < this.n; i++) {
            this.a[i].getStan();
        }
    }

    public void getMarkowe(int marka) {
        for (int i = 0; i < this.n; i++) {
            if (this.a[i].getMarka() == marka) {
                this.a[i].getStan();
            }
        }
    }

    public int getMostExpensive() {
        int max_cena = -1;
        int max_numer = -1;

        for (int i = 0; i < this.n; i++) {
            if (this.a[i].getCena() > max_cena) {
                max_cena = this.a[i].getCena();
                max_numer = this.a[i].getNrnadwozia();
            }
        }

        return max_numer;
    }

    public int getCountAllBelow2000() {
        int ile_aut = 0;
        for (int i = 0; i < this.n; i++) {
            if (this.a[i].getCena() < 2000) {
                ile_aut++;
            }
        }
        return ile_aut;
    }

    public void modifyPrice(int i) {
        if (i > this.n - 1) {
            return;
        }
        if (this.a[i].getCena() >= 4000) {
            this.a[i].setCena((int)(this.a[i].getCena() * 0.9));
        } else {
            this.a[i].setCena((int)(this.a[i].getCena() * 0.95));
        }
    }
}
