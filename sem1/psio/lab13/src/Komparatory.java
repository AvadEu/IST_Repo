import java.util.Comparator;

public class Komparatory {
    public static Comparator<Bryła> wedługKoloru = new Comparator<Bryła>() {
        @Override
        public int compare(Bryła b1, Bryła b2) {
            return b1.getKolor().compareTo(b2.getKolor());
        }
    };

    public static Comparator<Bryła> wedługWysokości = new Comparator<Bryła>() {
        @Override
        public int compare(Bryła b1, Bryła b2) {
            return Integer.compare(b1.getH(), b2.getH());
        }
    };

    public static Comparator<Bryła> wedługKoloruIWysokości = new Comparator<Bryła>() {
        @Override
        public int compare(Bryła b1, Bryła b2) {
            int result = b1.getKolor().compareTo(b2.getKolor());
            if (result == 0) {
                return Integer.compare(b1.getH(), b2.getH());
            }
            return result;
        }
    };
}
