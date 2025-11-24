package Zamówienie;

import Dostawa.SposóbDostawy;
import Płatność.SposóbPłatności;

public class ZamówienieHurtowe extends Zamówienie{
    private boolean czyFakturaVAT;
    private String NIP;

    public ZamówienieHurtowe(double wartość, double zniżka, boolean czyFaktura, String NIP) {
        super(wartość, zniżka);
        this.czyFakturaVAT = czyFaktura;
        this.NIP = NIP;
    }

    public void finalizujZamówienie(SposóbPłatności p, SposóbDostawy d) {
        super.setPłatność(p);
        double doZapłacenia = doZapłaty();
        boolean udane = p.pobraniePłatności(doZapłacenia);
        if (udane) {
            super.setZfinalizowane();
            d.potwierdźNadanie();
            System.out.println("Finalizacja udana!");
        } else {
            System.out.println("Błąd płatności!");
        }
    }

    public String toString() {
        return super.toString() + " NIP: " + this.NIP + " Faktura VAT: " + czyFakturaVAT;
    }
}
