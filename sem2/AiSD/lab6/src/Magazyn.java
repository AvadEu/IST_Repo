public class Magazyn {
    private IQueue<ZgloszenieKlienta> kolejkaZgloszen;
    private double calkowitaSumaKwot;

    public Magazyn() {
        this.kolejkaZgloszen = new LinkedListQueue<ZgloszenieKlienta>();
        this.calkowitaSumaKwot = 0.0;
    }

    public void dodajZgloszenie(ZgloszenieKlienta zgloszenie) {
        kolejkaZgloszen.enqueue(zgloszenie);
        System.out.println("Magazyn przyjął zgłoszenie od: " + zgloszenie.getNazwaKlienta());
    }

    public double getCalkowitaSumaKwot() {
        return calkowitaSumaKwot;
    }

    public void przetworzZgloszenia() {
        while (!kolejkaZgloszen.isEmpty()) {
            ZgloszenieKlienta aktualneZgloszenie = kolejkaZgloszen.dequeue();
            String nazwaKlienta = aktualneZgloszenie.getNazwaKlienta();
            IQueue<Zamowienie> kolejkaZamowienKlienta = aktualneZgloszenie.getKolejkaZamowienKlienta();

            System.out.println("\nPrzetwarzanie zgłoszenia klienta: " + nazwaKlienta);

            while (!kolejkaZamowienKlienta.isEmpty()) {
                Zamowienie zamowienie = kolejkaZamowienKlienta.dequeue();
                double kwotaZamowienia = zamowienie.obliczWartosc();
                calkowitaSumaKwot += kwotaZamowienia;

                String sformatowanaKwota = String.format("%.2f", kwotaZamowienia);

                System.out.println("Zlecenie zrealizowane: " + nazwaKlienta + ": " + zamowienie.getNazwaTowaru() + ", kwota do zapłaty = " + sformatowanaKwota);
            }
        }
        System.out.println("\n--- Podsumowanie ---");

        String sformatowanaCalkowitaSuma = String.format("%.2f", calkowitaSumaKwot);
        System.out.println("Suma po obsłudze wszystkich klientów: " + sformatowanaCalkowitaSuma);
    }
}
