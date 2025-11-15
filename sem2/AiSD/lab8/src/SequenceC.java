import java.util.ArrayList;

public class SequenceC {
    public static Integer [] getSeq(int n)
    {
        ArrayList<Integer> gaps = new ArrayList<>();
        int h = 0;
        gaps.add(h);
        gaps.add(1);
        for (int i = 1; h <= n; i++)
        {
            h = (int)Math.pow(2, i)+1;
            if (h <= n)
                gaps.add(h);
        }
        return gaps.toArray(new Integer[gaps.size()]);
    }

}