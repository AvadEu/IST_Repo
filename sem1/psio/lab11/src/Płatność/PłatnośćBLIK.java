package Płatność;

public class PłatnośćBLIK implements SposóbPłatności{
    private String numerTelefonu;
    private String kodBLIK;
    private boolean czyUdane;
    final static double LIMIT = 1500;
    private double wartość;

    public PłatnośćBLIK(String numerTelefonu, String kodBLIK) {
        this.numerTelefonu = numerTelefonu;
        this.kodBLIK = kodBLIK;
        this.czyUdane = false;
    }

    @Override
    public boolean pobraniePłatności(double wartość) {
        this.wartość = wartość;
        if (poprawyKod() && wartość < LIMIT) {
            this.czyUdane = true;
            return true;
        } else {
            return false;
        }
    }

    private boolean poprawyKod() {
        return this.kodBLIK.length() == 6;
    }

    public String getKodBLIK() {
        return kodBLIK;
    }

    public void setKodBLIK(String kodBLIK) {
        this.kodBLIK = kodBLIK;
    }

    public String getNumerTelefonu() {
        return numerTelefonu;
    }

    public void setNumerTelefonu(String numerTelefonu) {
        this.numerTelefonu = numerTelefonu;
    }

    public boolean isCzyUdane() {
        return czyUdane;
    }

    public void setCzyUdane(boolean czyUdane) {
        this.czyUdane = czyUdane;
    }

    public double getWartość() {
        return wartość;
    }

    public void setWartość(double wartość) {
        this.wartość = wartość;
    }

    public String toString() {
        return String.format("Płatność BLIK: %.2fzł Tel: %s | Udane: %b", this.wartość, this.numerTelefonu, this.czyUdane);
    }
}
