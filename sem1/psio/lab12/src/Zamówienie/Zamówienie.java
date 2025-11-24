package Zamówienie;

import Dostawa.SposóbDostawy;
import Płatność.SposóbPłatności;

import java.io.Serializable;

abstract public class Zamówienie implements Serializable {
    protected SposóbPłatności płatność;
    protected SposóbDostawy dostawa;

    private String data;
    private double zniżka;
    private double wartość;
    private static int counter = 0;
    private int id;
    private boolean zfinalizowane;

    public Zamówienie() {
        this.data = java.time.LocalDate.now().toString();
        this.id = ++counter;
        this.zfinalizowane = false;
    }

    public Zamówienie(double wartość, double zniżka) {
        this();
        this.wartość = wartość;
        this.zniżka = zniżka;
    }

    abstract public void finalizujZamówienie(SposóbPłatności p, SposóbDostawy d);

    public String toString() {
        return String.format("%d: %s | %.2fzł Zniżka: %3.2f", this.id, this.data, this.wartość, this.zniżka * 100) + "%" + " status: " + this.getStatus();
    }

    public double getWartość() {
        return this.wartość;
    }

    public double getZniżka() {
        return this.zniżka;
    }

    public double doZapłaty() {
        return this.wartość * this.zniżka;
    }

    public String getStatus() {
        if (this.zfinalizowane) {
            return "Ukończone";
        } else {
            return "Oczekuje na finalizację";
        }
    }

    public void setZfinalizowane() {
        this.zfinalizowane = true;
    }

    public boolean isZfinalizowane() {
        return this.zfinalizowane;
    }

    public SposóbPłatności getPłatność() {
        return this.płatność;
    }

    public void setPłatność(SposóbPłatności p) {
        this.płatność = p;
    }

    public SposóbDostawy getDostawa() {
        return this.dostawa;
    }

    public void setDostawa(SposóbDostawy d) {
        this.dostawa = d;
    }

    public static void setCounter(int new_counter) {
        counter = new_counter;
    }

    public int getId() {
        return this.id;
    }
 }
