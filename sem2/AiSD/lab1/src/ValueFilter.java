import java.util.ArrayList;
import java.util.Iterator;

public class ValueFilter {
    public static void apply(ArrayList<Karta> karty, int value) {
        Iterator<Karta> iterator = karty.iterator();
        while (iterator.hasNext()) {
            Karta karta = iterator.next();
            if (karta.getWartosc() == value) {
                System.out.println(karta.toString());
            }
        }
    }
}
