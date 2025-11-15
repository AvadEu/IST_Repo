public class Klient {
    private String nazwa;
    private IQueue<Zamowienie> kolejkaZamowien;

    public Klient(String nazwa) {
        this.nazwa = nazwa;
        this.kolejkaZamowien = new LinkedListQueue<Zamowienie>();
    }

    public void dodajZamowienie(Zamowienie zamowienie) {
        kolejkaZamowien.enqueue(zamowienie);
        System.out.println("Klient " + nazwa + " dodał zamówienie: " + zamowienie);
    }

    public ZgloszenieKlienta stworzZgloszenie() {
        return new ZgloszenieKlienta(this.nazwa, this.kolejkaZamowien);
    }

    public String getNazwa() {
        return nazwa;
    }
}
