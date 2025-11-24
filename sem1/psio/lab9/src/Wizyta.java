public class Wizyta {
    private int kodChoroby;
    private int cenaWizyty;
    private boolean wystawionoZwolnienie;
    private boolean wystawionoReceptę;

    public Wizyta() {
        this.kodChoroby = 0;
        this.cenaWizyty = 0;
        this.wystawionoZwolnienie = false;
        this.wystawionoReceptę = false;
    }

    public Wizyta(int kod, int cena, boolean zwolnienie, boolean recepta) {
        this.kodChoroby = kod;
        this.cenaWizyty = cena;
        this.wystawionoZwolnienie = zwolnienie;
        this.wystawionoReceptę = recepta;
    }

    public int getCenaWizyty() {
        return this.cenaWizyty;
    }

    public String toString() {
        return String.format("%2d %2d %b %b",
                this.kodChoroby, this.cenaWizyty, this.wystawionoZwolnienie, this.wystawionoReceptę);
    }
}
