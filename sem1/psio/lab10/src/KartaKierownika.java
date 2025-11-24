public class KartaKierownika extends KartaPracownika{

    public KartaKierownika() {
        super();
    }

    public KartaKierownika(int numer, String nazwisko) {
        super(numer, nazwisko);
    }

    @Override
    public double premia() {
        return 0.5;
    }
}
