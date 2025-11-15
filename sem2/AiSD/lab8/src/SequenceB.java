import java.util.ArrayList;

public class SequenceB {
    public static Integer [] getSeq(int n)
    {
        ArrayList<Integer> gaps = new ArrayList<>();
        int h = 0;
        for (int i=0; h<=n; i++)
        {
            h = (int)Math.pow(2, i)-1;
            if (h <= n)
                gaps.add(h);
        }
        return gaps.toArray(new Integer[gaps.size()]);
    }
}