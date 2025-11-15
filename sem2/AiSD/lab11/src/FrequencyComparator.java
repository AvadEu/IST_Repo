import java.util.Comparator;

public class FrequencyComparator implements Comparator<HuffmanNode> {

    @Override
    public int compare(HuffmanNode node1, HuffmanNode node2)
    {
        if (node1.getFrequency()!=node2.getFrequency())
            return node1.getFrequency()-node2.getFrequency();
        else
            return node1.nodes()-node2.nodes();
    }
}