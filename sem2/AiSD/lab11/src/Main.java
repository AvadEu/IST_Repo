import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws InvalidTreeException, InvalidArgumentException {

        Scanner scan = new Scanner(System.in);
        System.out.print("Plik z tekstem jawnym: ");
        String nazwa = scan.nextLine();
        System.out.print("Gdzie zapisać zakodowany tekst: ");
        String nazwa2 = scan.nextLine();

        String tekst = odczytZPliku(nazwa);
        HuffmanTree drz = drzewoHuffmana(tekst);
        drz.wyswietlKody();
        String encrypted = drz.szyfr(tekst);
        System.out.println("Tekst zakodowany: " + encrypted);
        zapisDoPliku(nazwa2, encrypted);
        System.out.println("Tekst odkodowany: " + drz.deszyfr(odczytZPliku(nazwa2)));
    }

    public static ArrayList<HuffmanNode> wystapienia(String s)
    {
        int [] encounters = new int[s.length()];
        char [] string = s.toCharArray();
        boolean [] tmp = new boolean[string.length];

        ArrayList<HuffmanNode> result = new ArrayList<>();

        for(int i = 0; i < s.length(); i++)
        {
            encounters[i] = 1;
            for(int j = i+1; j <s.length(); j++)
            {
                if(string[i] == string[j])
                {
                    encounters[i]++;
                    tmp[j]=true;
                }
            }
        }

        for (int i=0; i<encounters.length; i++)
        {
            if (!tmp[i])
            {
                result.add(new HuffmanNode(Character.toString(string[i]), encounters[i]));
            }
        }

        return result;
    }

    public static HuffmanTree drzewoHuffmana(String s) throws InvalidArgumentException
    {
        PriorityQueue<HuffmanNode> kolejka = new PriorityQueue<>(new FrequencyComparator());
        kolejka.addAll(wystapienia(s));
        while (kolejka.size()>1)
        {
            HuffmanNode n1 = kolejka.poll();
            HuffmanNode n2 = kolejka.poll();
            HuffmanNode n = new HuffmanNode(n1.getFrequency() + n2.getFrequency());
            n.setLeft(n1);
            n.setRight(n2);
            kolejka.add(n);
        }
        if (kolejka.peek()!=null)
        {
            return new HuffmanTree(kolejka.poll());
        }
        else
            throw new InvalidArgumentException();
    }

    public static String odczytZPliku(String plik)
    {
        StringBuilder sb = new StringBuilder();
        try (BufferedReader br = new BufferedReader(new FileReader("src/" + plik)))
        {
            String line;
            while((line = br.readLine())!=null)
            {
                sb.append(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return sb.toString();
    }

    public static void zapisDoPliku(String plik, String napis)
    {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter("src/" + plik)))
        {
            bw.write(napis);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}