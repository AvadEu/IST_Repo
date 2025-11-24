package Płatność;

import java.io.Serializable;

public class PłatnośćPrzelew implements SposóbPłatności, Serializable {
    private String odbiorca;
    private String numerIBAN;
    private double wartość;

    public PłatnośćPrzelew(String odbiorca, String numerIBAN) {
        this.odbiorca = odbiorca;
        this.numerIBAN = numerIBAN;
    }

    public boolean pobraniePłatności(double wartość) {
        this.wartość = wartość;
        return sumaKontrolna();
    }

    private boolean sumaKontrolna() {
        int n1 = this.numerIBAN.charAt(0) - '0';
        int n2 = this.numerIBAN.charAt(1) - '0';
        return ((n1 + n2 == 4) || (n1 + n2 == 7));
    }

    public String toString() {
        return String.format("Przelew: %.2fzł do %s %s", this.wartość, this.odbiorca, this.numerIBAN);
    }
}
