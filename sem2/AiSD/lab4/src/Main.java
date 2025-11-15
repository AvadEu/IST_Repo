import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        while (true) {

            System.out.println("Menu:");
            System.out.println("1. Sprawdź nawiasy");
            System.out.println("2. Sprawdź czy napis jest palindromem");
            System.out.println("3. Przeniesienie elementów stosu");
            System.out.println("4. Zakończ");

            int choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                    zadanieNawiasy();
                    break;
                case 2:
                    zadaniePalindrom();
                    break;
                case 3:
                    zadaniePrzeniesienie();
                    break;
                case 4:
                    System.exit(0);
            }
        }
    }

    public static void zadanieNawiasy() {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Podaj wyrażenie do sprawdzenia:");
        String text = scanner.nextLine();

        boolean wynik = Nawiasy.nawiasyZrownowazone(text);

        if (wynik) {
            System.out.println("POPRAWNE nawiasowanie.");
        } else {
            System.out.println("NIEPOPRAWNE nawiasowanie");
        }
    }

    public static void zadaniePalindrom() {
        Scanner sc = new Scanner(System.in);
        System.out.println("Podaj słowo:");
        String napis = sc.nextLine();

        if (napis == null || napis.isEmpty()) {
            System.out.println("NIE JEST palindromem.");
            return;
        }

        napis = napis.toLowerCase().replaceAll("\\s+", "");

        ArrayStack<Character> s1 = new ArrayStack<Character>(napis.length());
        ArrayStack<Character> s2 = new ArrayStack<Character>(napis.length());

        for (Character c : napis.toCharArray()) {
            s1.push(c);
            s2.push(c);
        }

        s2.odwroc();

        while (!s1.isEmpty()) {
            if (s1.pop() != s2.pop()) {
                System.out.println("NIE JEST palindromem.");
                return;
            }
        }
        System.out.println("JEST palindromem.");
    }

    public static void zadaniePrzeniesienie() {
        ArrayStack<String> s1 = new ArrayStack<String>(4);
        ArrayStack<String> s2 = new ArrayStack<String>(4);
        s1.push("4");
        s1.push("3");
        s1.push("2");
        s1.push("1");
        System.out.println("Przed przeniesieniem:");
        System.out.println("s1: " + s1.toString());
        System.out.println("s2: " + s2.toString());
        przeniesienie(s1, s2);
        System.out.println("Po przeniesieniu:");
        System.out.println("s1: " + s1.toString());
        System.out.println("s2: " + s2.toString());
    }

    public static void przeniesienie(ArrayStack<String> s1, ArrayStack<String> s2) {
        String tmp;
        if (s1.isEmpty()) {
            return;
        }
        tmp = s1.pop();
        przeniesienie(s1, s2);
        s2.push(tmp);
    }
}
