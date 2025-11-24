public class SamolotTowarowy extends Samolot {

    private int maxLoad;
    private int zasięg;

    public SamolotTowarowy(String marka, String model, int maxLoad, int zasięg) {
        super(marka, model);
        this.maxLoad = maxLoad;
        this.zasięg = zasięg;
    }

    public String toString() {
        return super.toString() + " maksymalna ładowność:" + maxLoad + "kg" + " zasięg: " + this.zasięg + "km";
    }

    public void getStan() {
        System.out.println(this.toString());
    }

}
