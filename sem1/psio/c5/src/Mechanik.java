public class Mechanik {
    public static void podbijPrzegląd(Car auto) {
        if (auto.jestSilnik()) {
            auto.setAktywnyPrzegląd(true);
        } else {
        }
    }
}
