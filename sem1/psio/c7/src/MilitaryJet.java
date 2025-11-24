public class MilitaryJet extends Plane{
    private String codename;
    private int rockets;

    public MilitaryJet(int altitude, String model, int fuel_capacity, String codename, int rockets) {
        super(altitude, model, fuel_capacity);
        this.codename = codename;
        this.rockets = rockets;
    }

    public String toString() {
        return super.toString() + " " + this.codename + " " + this.rockets;
    }

    public String getCodename() {
        return codename;
    }

    public void setCodename(String codename) {
        this.codename = codename;
    }

    public int getRockets() {
        return rockets;
    }

    public void setRockets(int rockets) {
        this.rockets = rockets;
    }
}
