import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        System.out.print("Podaj nazwę pliku wejściowego: ");
        String fileName = sc.nextLine();

        List<Edge> edges = new ArrayList<>();
        int n = 0, m = 0;

        try (Scanner scanner = new Scanner(new File(fileName))) {
            n = scanner.nextInt();
            m = scanner.nextInt();
            for (int i = 0; i < m; i++) {
                int from = scanner.nextInt();
                int to = scanner.nextInt();
                int weight = scanner.nextInt();
                if (weight > 500 || from > n || to > n || n > 20 || m > 190) {
                    System.out.println("Dane nie spełniają warunków!");
                    System.exit(0);
                }
                edges.add(new Edge(from, to, weight));
            }
        } catch (FileNotFoundException e) {
            System.out.println("Nie znaleziono pliku: " + fileName);
            return;
        }

        int result = Kruskal.findMST(n, edges);
        System.out.println("Minimalna długość kabla: " + result);
    }
}
