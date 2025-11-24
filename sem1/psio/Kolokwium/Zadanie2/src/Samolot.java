abstract public class Samolot {
    private String marka;
    private String model;

    public Samolot(String marka, String model) {
        this.marka = marka;
        this.model = model;
    }

    public String toString() {
        return marka + " " + model;
    }

    public void getStan() {
        System.out.println(this.toString());
    }
}
