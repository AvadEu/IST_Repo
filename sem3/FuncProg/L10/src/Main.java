import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            System.out.println("--- Generator Choinki ---");
            System.out.print("Podaj wysokość choinki (>= 2): ");
            int height = scanner.nextInt();
            scanner.nextLine();

            ChristmasTree myTree = new PineTree(height);
            System.out.println("\nChoinka przed dekoracją:");
            System.out.println(myTree);

            System.out.println("Dostępne dekoracje: baubles, lights, angel");
            System.out.print("Wybierz dekorację: ");
            String decoChoice = scanner.nextLine();

            DecorationFactory factory = new DecorationFactory();
            IDecoration decoration = factory.getDecoration(decoChoice);

            System.out.println("\nDodajemy dekorację: " + decoration);
            myTree.applyDecoration(decoration);

            System.out.println("Choinka po dekoracji:");
            System.out.println(myTree);

        } catch (Exception e) {
            System.err.println("Błąd: " + e.getMessage());
        }
//        Tests.runTests();
    }
}