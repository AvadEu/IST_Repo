public abstract class FlyingVechicle {
    private String kind;
    private int altitude;

    public FlyingVechicle(String name, int altitude) {
        this.kind = name;
        this.altitude = altitude;
    }


    public String toString() {
        return this.kind + ": " + this.altitude + "m";
    }
}
