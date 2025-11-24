public class Baloon extends FlyingVechicle{
    private int people_capacity;
    private String color;
    private Passenger[] passengers;

    public Baloon(int altitude, int people_capacity, String color) {
        super("Baloon", altitude);
        this.people_capacity = people_capacity;
        this.color = color;
        this.passengers = new Passenger[people_capacity];
    }

    public String toString() {
        return super.toString() + " " + this.people_capacity + " people, " + this.color + "\nPassengers:" + getPassengers();
    }

    public String getPassengers() {
        String output = "";
        for (int i = 0; i < passengers.length; i++) {
            if (passengers[i] != null) {
                output +=  "\n" + passengers[i].toString();
            }
        }
        return output;
    }

    public void addPassenger(Passenger passenger) {
        for (int i = 0; i < passengers.length; i++) {
            if (passengers[i] == null) {
                passengers[i] = passenger;
                break;
            }
        }
    }

    public int getPeople_capacity() {
        return people_capacity;
    }

    public void setPeople_capacity(int people_capacity) {
        this.people_capacity = people_capacity;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }

}
