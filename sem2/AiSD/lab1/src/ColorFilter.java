import java.util.ArrayList;
import java.util.Iterator;

public class ColorFilter {
    public static void apply(ArrayList<Karta> karty, int color) {
        Iterator<Karta> iterator = karty.iterator();
        while (iterator.hasNext()) {
            Karta karta = iterator.next();
            if (karta.getKolor() == color) {
                System.out.println(karta.toString());
            }
        }
    }
}