import java.util.Scanner;

public class Tablice {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();

        int tablica [][] = new int[n][];

        for (int i = 0; i < n; i++) {
            tablica[i] = new int[i+1];
            for (int j = 0; j <= i; j++) {
                tablica[i][j] = j+1;
            }
        }

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < tablica[i].length; j++) {
                System.out.printf("%d ", tablica[i][j]);
            }
            System.out.println();
        }
    }
}
