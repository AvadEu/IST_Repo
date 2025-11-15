import java.util.ArrayList;

public class SequenceFib {
    public static Integer [] getSeq(int n)
    {
        ArrayList<Integer> gaps = new ArrayList<>();
        int h = 1;
        int ppn, pn = 0;
        gaps.add(pn);
        for (int i = 1; h <= n; i++)
        {
            ppn = pn;
            pn = h;
            h = ppn + pn;
            if (h <= n)
                gaps.add(h);
        }
        return gaps.toArray(new Integer[gaps.size()]);
    }
}
