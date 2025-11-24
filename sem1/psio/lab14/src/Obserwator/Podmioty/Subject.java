package Obserwator.Podmioty;

import Obserwator.Inwestorzy.Observer;

public interface Subject {
    public void registerObserver(Observer o);
    public void removeObserver(Observer o);
    public void notifyObservers();
}
