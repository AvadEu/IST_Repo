package Płatność;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class PłatnośćPayPal implements SposóbPłatności{
    private String email;
    private double wartość;

    public PłatnośćPayPal(String email) {
        this.email = email;
    }

    public boolean pobraniePłatności(double wartość) {
        this.wartość = wartość;
        return poprawnyEmail();
    }

    private boolean poprawnyEmail() {
        String emailRegex = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$";
        Pattern pattern = Pattern.compile(emailRegex);
        Matcher matcher = pattern.matcher(this.email);
        return matcher.matches();
    }

    public String toString() {
        return String.format("PayPal: %s, %.2fzł", this.email, this.wartość);
    }
}
