public class ZgloszenieKlienta {
    private String nazwaKlienta;
    private IQueue<Zamowienie> kolejkaZamowienKlienta;

    public ZgloszenieKlienta(String nazwaKlienta, IQueue<Zamowienie> kolejkaZamowienKlienta) {
        this.nazwaKlienta = nazwaKlienta;
        this.kolejkaZamowienKlienta = kolejkaZamowienKlienta;
    }

    public String getNazwaKlienta() {
        return nazwaKlienta;
    }

    public IQueue<Zamowienie> getKolejkaZamowienKlienta() {
        return kolejkaZamowienKlienta;
    }
}

