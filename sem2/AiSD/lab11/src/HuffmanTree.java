import java.util.HashMap;
import java.util.Map;

public class HuffmanTree {

    HuffmanNode root;

    public HuffmanTree(HuffmanNode root)
    {
        this.root = root;
    }

    private void kody(HuffmanNode elem, String s, HashMap<HuffmanNode, String> codes)
    {
        if (elem != null)
        {
            if (elem.getRight() != null)
                kody(elem.getRight(), s+"1", codes);
            if (elem.getLeft() != null)
                kody(elem.getLeft(), s+"0", codes);
            if (elem.getLeft() == null && elem.getRight() == null)
                codes.put(elem, s);
        }
    }

    public HashMap<HuffmanNode, String> Codes()
    {
        HashMap<HuffmanNode, String> kody = new HashMap<>();
        kody(root, "", kody);
        return kody;
    }

    public void wyswietlKody()
    {
        HashMap<HuffmanNode, String> mapa = this.Codes();
        mapa.entrySet().stream().sorted(Map.Entry.comparingByKey()).forEach(e -> System.out.println(e.getKey() + "\t" + e.getValue()));
    }

    public HashMap<String, String> codes()
    {
        HashMap<HuffmanNode, String> mapa = this.Codes();
        HashMap<String, String> map2 = new HashMap<>();
        for (Map.Entry<HuffmanNode,String> entry : mapa.entrySet())
            map2.put(entry.getKey().getValue(), entry.getValue());
        return map2;
    }

    public String szyfr(String s) throws InvalidTreeException
    {
        HashMap<String, String> kody = this.codes();
        StringBuilder sb = new StringBuilder();

        for (int i=0; i<s.length(); i++)
        {
            if (kody.containsKey(Character.toString(s.charAt(i))))
                sb.append(kody.get(Character.toString(s.charAt(i))));
            else
                throw new InvalidTreeException();
        }
        return sb.toString();
    }

    public String deszyfr(String s) throws InvalidTreeException
    {
        StringBuilder sb = new StringBuilder();
        HuffmanNode akt = root;
        int i = 0;
        while(i < s.length())
        {
            if (akt.getLeft() == null && akt.getRight() == null)
            {
                if (akt.getValue() != null)
                {
                    sb.append(akt.getValue());
                    akt = root;
                }
                else
                    throw new InvalidTreeException();
            }
            else
            {
                if (s.charAt(i) == '0')
                    akt=akt.getLeft();
                if (s.charAt(i) == '1')
                    akt=akt.getRight();
                i++;
            }
        }
        if (akt.getValue() != null)
            sb.append(akt.getValue());
        else
            throw new InvalidTreeException();
        return sb.toString();
    }

}