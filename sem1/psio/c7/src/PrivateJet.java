public class PrivateJet extends Plane {
    private double price;
    private int seats;

    public PrivateJet(String model, int altitude, int fuel_capacity, double price, int seats) {
        super(altitude, model, fuel_capacity);
        this.price = price;
        this.seats = seats;
    }

    public String toString() {
        return super.toString() + " " + this.price + "zł " + seats + " miejsca";
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public int getSeats() {
        return seats;
    }

    public void setSeats(int seats) {
        this.seats = seats;
    }
}
