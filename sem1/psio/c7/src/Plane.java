abstract public class Plane extends FlyingVechicle{
    private String model;
    private int fuel_capacity;
    private boolean readyToFlight;

    Plane(int altitude, String model, int fuel_capacity) {
        super("Samolot", altitude);
        this.model = model;
        this.fuel_capacity = fuel_capacity;
        this.readyToFlight = false;
    }

    public String toString() {
        return super.toString() + " " + this.model + " " + this.fuel_capacity + "l Sprawny: " + this.readyToFlight;
    }

    public boolean isReadyToFlight() {
        return readyToFlight;
    }

    public void setReadyToFlight(boolean readyToFlight) {
        this.readyToFlight = readyToFlight;
    }

}
