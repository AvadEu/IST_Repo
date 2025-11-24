public class Auto {
    private int nrnadwozia;
    private int marka;
    private int cena;
    private static int ile = 0;

    public static int getIle() {
        return Auto.ile;
    }

    public int getCena() {
        return cena;
    }

    public void setCena(int cena) {
        this.cena = cena;
    }

    public int getMarka() {
        return marka;
    }

    public void setMarka(int marka) {
        this.marka = marka;
    }

    public int getNrnadwozia() {
        return nrnadwozia;
    }

    public Auto() {
        ile++;
        this.nrnadwozia = ile;
    }

    public Auto(int marka, int cena) {
        this();
        this.marka = marka;
        this.cena = cena;
    }

    public void getStan() {
        System.out.printf("nrnadwozia: %d marka: %d cena: %d\n", this.nrnadwozia, this.marka, this.cena);
    }
}
