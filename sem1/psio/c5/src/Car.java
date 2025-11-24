public class Car {
    private int rokProdukcji;
    private int przebieg;
    private String marka;
    private String model;
    private String typ;
    private boolean aktywnyPrzegląd;
    private Silnik silnik;

    public Car() {
        this.silnik = new Silnik();
        this.rokProdukcji = 2024;
        this.marka = "Skoda";
        this.model = "Fabia";
        this.typ = "Hatchback";
        this.aktywnyPrzegląd = false;
        this.przebieg = 0;
    }

    public Car(int rokProdukcji, int przebieg, String marka, String model, String typ) {
        this();
        this.rokProdukcji = rokProdukcji;
        this.przebieg = przebieg;
        this.marka = marka;
        this.model = model;
        this.typ = typ;
    }

    public int getRokProdukcji() {
        return rokProdukcji;
    }

    public void setRokProdukcji(int rokProdukcji) {
        this.rokProdukcji = rokProdukcji;
    }

    public int getPrzebieg() {
        return przebieg;
    }

    public void setPrzebieg(int przebieg) {
        this.przebieg = przebieg;
    }

    public String getMarka() {
        return marka;
    }

    public void setMarka(String marka) {
        this.marka = marka;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public String getTyp() {
        return typ;
    }

    public void setTyp(String typ) {
        this.typ = typ;
    }

    public boolean isAktywnyPrzegląd() {
        return aktywnyPrzegląd;
    }

    public void setAktywnyPrzegląd(boolean aktywnyPrzegląd) {
        this.aktywnyPrzegląd = aktywnyPrzegląd;
    }

    public Silnik getSilnik() {
        return silnik;
    }

    public void setSilnik(Silnik silnik) {
        this.silnik = silnik;
    }

    public boolean jestSilnik() {
        if (this.silnik != null) {
            return true;
        } else {
            return false;
        }
    }

    public void getStan() {
        System.out.println("przebieg: " + przebieg);
        System.out.println("marka: " + marka);
        System.out.println("model: " + model);
        System.out.println("typ: " + typ);
        System.out.println("czyAktywnyPrzegląd: " + aktywnyPrzegląd);
        System.out.println("Silnik: ");
        if (this.jestSilnik()) {
            silnik.getStan();
        } else {
            System.out.println("Brak silnika!");
        }

    }
}
