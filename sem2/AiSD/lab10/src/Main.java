import java.io.IOException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        RBTree tree = new RBTree();

        System.out.print("Podaj nazwę pliku tekstowego: ");
        Scanner sc = new Scanner(System.in);
        String filename = sc.nextLine();

        try {
            FileParser.parseFile(filename, tree);
        } catch (IOException e) {
            System.out.println("Błąd odczytu pliku: " + e.getMessage());
            return;
        }
        while (true) {

            System.out.println("Wybierz operację:");
            System.out.println("1. Skorowidz");
            System.out.println("2. Przejście BFS");
            System.out.println("3. Usunięcie węzła");
            System.out.println("4. Koniec");

            int choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                    System.out.println("Skorowidz:");
                    tree.inOrderPrint();
                    break;
                case 2:
                    System.out.println("\nZastosowanie algorytmu BFS:");
                    tree.bfsPrint();
                    break;
                case 3:
                    System.out.println("\n Podaj słowo do usunięcia: ");
                    String word = sc.nextLine();
                    tree.delete(word);
                    System.out.println("Poprawnie usunięto węzeł [" + word + "]");

                    System.out.println("Skorowidz:");
                    tree.inOrderPrint();
                    break;
                case 4:
                    System.exit(0);
                default:
                    System.out.println("Nieprawidłowa instrukcja!");
            }
        }
    }
}
