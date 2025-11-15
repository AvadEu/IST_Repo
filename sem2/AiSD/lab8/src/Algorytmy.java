import java.util.Arrays;
import java.util.Random;

public class Algorytmy {

    private int [] los;

    public Algorytmy(int n)
    {
        this.los = new int[n];

        for (int i=0; i<los.length; i++)
        {
            Random gen = new Random();
            int el = gen.nextInt(n+1);
            los[i] = el;
        }
    }

    private int [] utworz(int [] array)
    {
        int [] tmp = new int[array.length];
        System.arraycopy(array, 0, tmp, 0, array.length);
        return tmp;
    }

    private void shellsort1(int [] array, Integer[] distances)
    {
        int n = array.length;
        int iteration = 1;
        int actDistance = distances[distances.length-iteration];
        int comp, cur;

        while (actDistance >= 1)
        {
            for (int i = actDistance; i < n; i++)
            {
                cur = array[i];
                comp = i;
                while (comp >= actDistance && cur < array[comp-actDistance])
                {
                    array[comp] = array[comp-actDistance];
                    comp -= actDistance;
                }
                array[comp] = cur;
            }
            actDistance = distances[distances.length-++iteration];
        }
    }

    public void ShellSort1()
    {
        System.out.println("Algorytm 1:");

        int [] tmp;
        tmp = utworz(los);
        Integer [] dystanse = SequenceA.getSeq(los.length);
        long t1 = System.nanoTime();
        shellsort1(tmp, dystanse);
        long t2 = System.nanoTime();
        long t = (t2-t1) / 10;
        System.out.println("Wynik dla ciągu a: " + t);

        tmp = utworz(los);
        dystanse = SequenceB.getSeq(los.length);
        t1 = System.nanoTime();
        shellsort1(tmp, dystanse);
        t2 = System.nanoTime();
        t = (t2-t1);
        System.out.println("Wynik dla ciągu b: " + t);

        tmp = utworz(los);
        dystanse = SequenceC.getSeq(los.length);
        t1 = System.nanoTime();
        shellsort1(tmp, dystanse);
        t2 = System.nanoTime();
        t = (t2-t1);
        System.out.println("Wynik dla ciągu c: " + t);

        tmp = utworz(los);
        dystanse = SequenceFib.getSeq(los.length);
        t1 = System.nanoTime();
        shellsort1(tmp, dystanse);
        t2 = System.nanoTime();
        t = (t2-t1);
        System.out.println("Wynik dla ciągu d: " + t);

        tmp = utworz(los);
        dystanse = SequenceNew.getSeq(los.length);
        t1 = System.nanoTime();
        shellsort1(tmp, dystanse);
        t2 = System.nanoTime();
        t = (t2-t1);
        System.out.println("Wynik dla ciągu dodatkowy: " + t + "\n");
    }

    private void bubblesort(int [] tabl)
    {
        int size = tabl.length;
        for (int i = 0; i < size-1; i++)
        {
            for (int j = 0; j < size-i-1; j++)
            {
                if (tabl[j] > tabl[j+1])
                    swap(tabl, j+1, j);
            }
        }
    }

    private void swap(int [] tabl, int left, int right)
    {
        int temp = tabl[left];
        tabl[left] = tabl[right];
        tabl[right] = temp;
    }

    private void shellsort2(int [] array, Integer [] distances)
    {
        int n = array.length;
        int iteration = 1;
        int actDistance = distances[distances.length-iteration];
        int comp, cur;

        while (actDistance > 1)
        {
            if (actDistance != 1)
            {
                for (int i=actDistance; i<n; i++)
                {
                    cur = array[i];
                    comp = i;
                    while (comp >= actDistance && cur < array[comp-actDistance])
                    {
                        array[comp] = array[comp-actDistance];
                        comp -= actDistance;
                    }
                    array[comp] = cur;
                }
            }
            iteration++;
            actDistance = distances[distances.length-iteration];
        }
        if (actDistance == 1)
            bubblesort(array);
    }

    public void ShellSort2()
    {
        System.out.println("Algorytm 2:");

        int [] tmp;
        tmp = utworz(los);
        Integer [] dystanse = SequenceA.getSeq(los.length);
        long t1 = System.nanoTime();
        shellsort2(tmp, dystanse);
        long t2 = System.nanoTime();
        long t = (t2-t1);
        System.out.println("Wynik dla ciągu a:" + t);

        tmp = utworz(los);
        dystanse = SequenceB.getSeq(los.length);
        t1 = System.nanoTime();
        shellsort2(tmp, dystanse);
        t2 = System.nanoTime();
        t = (t2-t1);
        System.out.println("Wynik dla ciągu b: " + t);

        tmp = utworz(los);
        dystanse = SequenceC.getSeq(los.length);
        t1 = System.nanoTime();
        shellsort2(tmp, dystanse);
        t2 = System.nanoTime();
        t = (t2-t1);
        System.out.println("Wynik dla ciągu c: " + t);

        tmp = utworz(los);
        dystanse = SequenceFib.getSeq(los.length);
        t1 = System.nanoTime();
        shellsort2(tmp, dystanse);
        t2 = System.nanoTime();
        t = (t2-t1);
        System.out.println("Wynik dla ciągu d: " + t);

        tmp = utworz(los);
        dystanse = SequenceNew.getSeq(los.length);
        t1 = System.nanoTime();
        shellsort2(tmp, dystanse);
        t2 = System.nanoTime();
        t = (t2-t1);
        System.out.println("Wynik dla ci dodatkowy: " + t + "\n");
    }

    private void shellsort3(int [] array, Integer [] distances)
    {
        int n = array.length;
        int iteration = 1;
        int actDistance = distances[distances.length-iteration];
        int comp, cur;

        while (actDistance>1)
        {
            if (actDistance != 1)
            {
                for (int i = actDistance; i < n; i++)
                {
                    cur = array[i];
                    comp = i;
                    while (comp >= actDistance)
                    {
                        if (cur < array[comp - actDistance])
                            swap(array, comp, comp-actDistance);
                        comp -= actDistance;
                    }
                }
            }
            iteration++;
            actDistance = distances[distances.length-iteration];
        }
        if (actDistance==1)
        {
//            System.out.println(Arrays.toString(array));
            insertsort(array);
        }
    }

    public void ShellSort3()
    {
        System.out.println("Algorytm 3:");

        int [] tmp;
        tmp = utworz(los);
        Integer [] dystanse = SequenceA.getSeq(los.length);
        long t1 = System.nanoTime();
        shellsort3(tmp, dystanse);
        long t2 = System.nanoTime();
        long t = (t2-t1);
        System.out.println("Wynik dla ciągu a:" + t);

        tmp = utworz(los);
        dystanse = SequenceB.getSeq(los.length);
        t1 = System.nanoTime();
        shellsort3(tmp, dystanse);
        t2 = System.nanoTime();
        t = (t2-t1);
        System.out.println("Wynik dla ciągu b: " + t);

        tmp = utworz(los);
        dystanse = SequenceC.getSeq(los.length);
        t1 = System.nanoTime();
        shellsort3(tmp, dystanse);
        t2 = System.nanoTime();
        t = (t2-t1);
        System.out.println("Wynik dla ciągu c: " + t);

        tmp = utworz(los);
        dystanse = SequenceFib.getSeq(los.length);
        t1 = System.nanoTime();
        shellsort3(tmp, dystanse);
        t2 = System.nanoTime();
        t = (t2-t1);
        System.out.println("Wynik dla ciągu d: " + t);

        tmp = utworz(los);
        dystanse = SequenceNew.getSeq(los.length);
        t1 = System.nanoTime();
        shellsort3(tmp, dystanse);
        t2 = System.nanoTime();
        t = (t2-t1);
        System.out.println("Wynik dla ciągu: " + t + "\n");
    }

    private void insertsort(int [] array)
    {
        for (int i = 1; i < array.length; ++i)
        {
            int value = array[i];
            int j;
            int temp;
            for (j = i; (j>0 && value<(temp=array[j-1])); --j)
            {
                array[j] = temp;
            }
            array[j] = value;
        }
    }

    public void wyswietl()
    {
        System.out.println(Arrays.toString(SequenceA.getSeq(100000)));
        System.out.println(Arrays.toString(SequenceB.getSeq(100000)));
        System.out.println(Arrays.toString(SequenceC.getSeq(100000)));
        System.out.println(Arrays.toString(SequenceFib.getSeq(100000)));
    }

}