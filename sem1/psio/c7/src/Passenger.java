public class Passenger {
    private String name;
    private int weight;

    public Passenger(String name, int weight) {
        this.name = name;
        this.weight = weight;
    }

    public String toString() {
        return this.name + " " + this.weight + "kg";
    }
}
