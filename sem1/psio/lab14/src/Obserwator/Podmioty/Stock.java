package Obserwator.Podmioty;

import Obserwator.Inwestorzy.Observer;

import java.util.ArrayList;

public class Stock implements Subject{

    private String name;
    private double price;

    final private ArrayList<Observer> observers;

    public Stock() {
        observers = new ArrayList<>();
    }

    public Stock(String name, double price) {
        this();
        this.name = name;
        this.price = price;
    }

    public void priceChange(double price) {
        this.price = price;
        notifyObservers();
    }

    public void registerObserver(Observer o) {
        observers.add(o);
    }

    public void removeObserver(Observer o) {
        observers.remove(o);
    }

    public void notifyObservers() {
        for (Observer o : observers) {
            o.update(this.name, this.price);
        }
    }
}
