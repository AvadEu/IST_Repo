public class SamolotOsobowy extends Samolot {

    private Pasażer[] pasażerowie;
    private int limitOsób;
    private int osobyNaPokładzie;

    public SamolotOsobowy(String marka, String model, int limitOsób) {
        super(marka, model);
        this.limitOsób = limitOsób;
        this.pasażerowie = new Pasażer[limitOsób];
        this.osobyNaPokładzie = 0;
    }

    public void dodajPasażera(Pasażer pasażer) {
        if (osobyNaPokładzie < limitOsób) {
            this.pasażerowie[osobyNaPokładzie] = pasażer;
            osobyNaPokładzie++;
        }
    }

    public String toString() {
        return super.toString() + " Limit Osób: " + this.limitOsób + " Osoby na pokładzie: " + osobyNaPokładzie;
    }

    public void getStan() {
        System.out.println(this.toString());
        System.out.println("Pasażerowie: ");
        for (int i = 0; i < osobyNaPokładzie; i++) {
            System.out.println(pasażerowie[i].toString());
        }
    }

}
