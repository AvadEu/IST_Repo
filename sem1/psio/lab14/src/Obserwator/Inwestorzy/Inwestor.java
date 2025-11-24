package Obserwator.Inwestorzy;

public class Inwestor implements Observer {
    private String name;
    private int age;
    private double money;
    private String country;
    private int stocks;

    public Inwestor(String name, int age, double money, String country) {
        this.name = name;
        this.age = age;
        this.money = money;
        this.country = country;
        this.stocks = 0;
    }

    public void update(String name, double price) {
        marketMove(name, price);
    }

    private void marketMove(String name, double price) {
        if (price < money / 2) {
            stocks++;
            money -= price;
            System.out.println(this.toString() + " -> Zakup akcji [" + name + "]");
        } else {
            System.out.println(this.toString() + " -> Akcja [" + name + "] za droga");
        }
    }

    public String toString() {
        return String.format("%s [%d] z %s - %.2f zł. Akcje: %d", name, age, country, money, stocks);
    }
}
