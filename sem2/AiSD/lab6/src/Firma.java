public class Firma {

    private double przychodyFirmy;
    private final IQueue<Magazyn> magazyny;

    public Firma() {
        magazyny = new LinkedListQueue<Magazyn>();
    }

    public void dodajMagazyn(Magazyn magazyn) {
        magazyny.enqueue(magazyn);
    }

    public IQueue<Magazyn> getMagazyny() {
        return magazyny;
    }

    public double getPrzychodyFirmy() {
        while(!magazyny.isEmpty()) {
            Magazyn aktualnyMagazyn = magazyny.dequeue();
            aktualnyMagazyn.przetworzZgloszenia();
            double aktualnaSuma = aktualnyMagazyn.getCalkowitaSumaKwot();
            przychodyFirmy += aktualnaSuma;
        }
        return przychodyFirmy;
    }
}
