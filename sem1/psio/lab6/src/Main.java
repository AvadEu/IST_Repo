import java.util.Random;

public class Main {
    public static void main(String[] args) {

        Random rand = new Random();

        Student[] Uczelnia = new Student[100];

        for (int i = 0; i < Uczelnia.length; i++) {
            double srednia = 2.0 + (new Random().nextInt(4) + new Random().nextDouble());
            Uczelnia[i] = new Student(i + 1, srednia);
        }

        allStudents(Uczelnia);
        
        int[] prymusi = bestStudents(Uczelnia);
        System.out.println("Prymusi:");

        for (int i = 0; i < prymusi.length; i++) {
            Uczelnia[prymusi[i]].getStan();
        }
    }

    public static void allStudents(Student[] Uczelnia) {
        for (int i = 0; i < Uczelnia.length; i++) {
            Uczelnia[i].getStan();
        }
    }

    public static int[] bestStudents(Student[] Uczelnia) {
        double maxSrednia = 0;
        int liczba_prymusow = 1;

        for (int i = 0; i < Uczelnia.length; i++) {
            if (maxSrednia < Uczelnia[i].getSrednia_ocen()) {
                maxSrednia = Uczelnia[i].getSrednia_ocen();
                liczba_prymusow = 1;
            } else if (maxSrednia == Uczelnia[i].getSrednia_ocen()) {
                liczba_prymusow++;
            }
        }

        int[] prymusi = new int[liczba_prymusow];
        int j = 0;

        System.out.printf("Średnia: %2.2f%n", maxSrednia);

        for (int i = 0; i < Uczelnia.length; i++) {
            if (Uczelnia[i].getSrednia_ocen() == maxSrednia) {
                prymusi[j] = i;
                j++;
            }
        }
        return prymusi;
    }
}