public class HuffmanNode implements Comparable<HuffmanNode>{

    private String value;
    private int frequency;
    private HuffmanNode left;
    private HuffmanNode right;

    public HuffmanNode(String value, int frequency)
    {
        this.value = value;
        this.frequency = frequency;
        this.left = null;
        this.right = null;
    }

    public HuffmanNode(int frequency)
    {
        this.value = null;
        this.frequency = frequency;
        this.left = null;
        this.right = null;
    }

    public String getValue()
    {
        return value;
    }

    public void setValue(String value)
    {
        this.value = value;
    }

    public int getFrequency() {
        return frequency;
    }

    public void setFrequency(int frequency) {
        this.frequency = frequency;
    }

    public HuffmanNode getLeft()
    {
        return left;
    }

    public void setLeft(HuffmanNode left)
    {
        this.left = left;
    }

    public HuffmanNode getRight()
    {
        return right;
    }

    public void setRight(HuffmanNode right)
    {
        this.right = right;
    }

    public int nodes()
    {
        int count = 0;
        count++;
        if (this.getLeft() != null)
            count += this.getLeft().nodes();
        if (this.getRight() != null)
            count += this.getRight().nodes();
        return count;
    }

    public int leaves()
    {
        int count=0;
        if (this.getLeft() == null && this.getRight() == null)
            count++;
        if (this.getLeft() != null)
            count += this.getLeft().leaves();
        if (this.getRight() != null)
            count += this.getLeft().leaves();

        return count;
    }

    public String toString()
    {
        return (this.getValue() + " - " + this.getFrequency());
    }

    @Override
    public int compareTo(HuffmanNode o)
    {
        return o.getFrequency()-this.getFrequency();
    }
}