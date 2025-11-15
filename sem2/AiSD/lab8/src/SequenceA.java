import java.util.ArrayList;

public class SequenceA {
    public static Integer [] getSeq(int n)
    {
        ArrayList<Integer> gaps = new ArrayList<>();
        int h = 0;
        while (h <= n)
        {
            gaps.add(h);
            h=3*h+1;
        }
        return gaps.toArray(new Integer[gaps.size()]);
    }
}
