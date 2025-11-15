import java.util.ArrayList;
import java.util.Collections;

public class SequenceNew {
    public static Integer [] getSeq(int n)
    {
        ArrayList<Integer> distances = new ArrayList<>();
        int h = n/2;
        distances.add(h);
        while (h != 1)
        {
            h *= 0.75;
            distances.add(h);
        }
        distances.add(0);
        Collections.reverse(distances);
        return distances.toArray(new Integer[distances.size()]);
    }
}
