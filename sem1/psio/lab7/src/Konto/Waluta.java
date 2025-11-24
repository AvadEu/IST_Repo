package Konto;

public class Waluta {
    private int nazwa;

    public Waluta() {
        this.nazwa = 1;
    }

    public Waluta(int nazwa) {
        this.nazwa = nazwa;
    }

    public int getNazwa() {
        return nazwa;
    }

    public String getStan() {
        switch (this.nazwa) {
            case 1:
                return "PLN";
            case 2:
                return "USD";

            case 3:
                return "EUR";
            default:
                return "PLN";
        }
    }
}
