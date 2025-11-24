package Zamówienie;

import Dostawa.SposóbDostawy;
import Płatność.SposóbPłatności;

public class ZamówienieDetaliczne extends Zamówienie {
    private boolean zapakowaćNaPrezent;
    private boolean zapakowane;

    public ZamówienieDetaliczne(double wartość, double zniżka, boolean zapakować) {
        super(wartość, zniżka);
        this.zapakowaćNaPrezent = zapakować;
        this.zapakowane = false;
    }

    public void finalizujZamówienie(SposóbPłatności p, SposóbDostawy d) {
        super.setPłatność(p);
        boolean udane = p.pobraniePłatności(doZapłaty());

        if (zapakowaćNaPrezent) {
            zapakujNaPrezent();
        }

        if (udane) {
            super.setZfinalizowane();
            d.potwierdźNadanie();
            System.out.println("Finalizacja udana!");

        } else {
            System.out.println("Błąd płatności!");
        }
    }

    public void zapakujNaPrezent() {
        this.zapakowane = true;
    }

    public String toString() {
        return super.toString() + " Zapakowane na prezent: " + zapakowaćNaPrezent;
    }
}
