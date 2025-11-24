import java.util.Arrays;
import java.util.Random;

public class Zadania {

    private final static Random rand = new Random();

    public static void Zadanie1() {
        int arr[] = new int[10];

        fillWithRandom(arr, 1, 10);

        System.out.printf("Tablica nie posortowana:%n%s%n", Arrays.toString(arr));
        BubbleSort.sort(arr);
        System.out.printf("Tablica posortowana:%n%s%n", Arrays.toString(arr));
    }

    public static void Zadanie2() {
        int[][] arr = new int[10][20];

        for (int i = 0; i < arr.length; i++) {
            fillWithRandom(arr[i], 1, 10);
        }

        print2DArray(arr, "Tablica nieposortowana:");

        for (int i = 0; i < arr.length; i++) {
            BubbleSort.sort(arr[i]);
        }

        print2DArray(arr, "Tablica posortowana:");

    }

    public static void Zadanie3() {
        int[] arr1 = new int[10];
        int[] arr2 = new int[10];

        fillWithRandom(arr1, 1, 10);
        fillWithRandom(arr2, 1, 10);

        System.out.printf("Tablica 1: %s%n", Arrays.toString(arr1));
        System.out.printf("Tablica 2: %s%n", Arrays.toString(arr2));

        int output = 0;

        for (int i = 0; i < arr1.length; i++) {
            int isDivisible = 0;
            for (int j = 0; j < arr2.length; j++) {
                if (arr1[i] % arr2[j] == 0) {
                    isDivisible++;
                }
            }
            if (isDivisible >= 3) {
                output++;
            }
        }
        System.out.printf("Ilość liczb z tablicy 1 podzielnych przez co najmniej 3 wartości z tablicy 2 wynosi: %2d", output);
    }

    public static void Zadanie4() {
        int[][] arr = new int[10][20];

        for (int i = 0; i < arr.length; i++) {
            fillWithRandom(arr[i], 1, 10);
        }

        print2DArray(arr, "Tablica nieposortowana:");
        arr = transpose(arr);

        for (int i = 0; i < arr.length; i++) {
            BubbleSort.sort(arr[i]);
        }

        arr = transpose(arr);
        print2DArray(arr, "Tablica posortowana:");

    }

    public static void Zadanie5() {
        int n = 10;

        int[][] arr = new int[n][];

        for (int i = 0; i < arr.length; i++) {
            arr[i] = new int[rand.nextInt(9) + 1];
            fillWithRandom(arr[i], 1, n);
        }

//        for (int i = 0; i < arr.length; i++) {
//            fillWithRandom(arr[i], 1, 10);
//        }

        print2DArray(arr, "Tablica nieposortowana:");

        for (int i = 0; i < arr.length; i++) {
            BubbleSort.sort(arr[i]);
        }

        print2DArray(arr, "Tablica posortowana:");
    }

    public static void Zadanie6() {
        int[][] R = new int[5][5];

        for (int i = 0; i < R.length; i++) {
            for (int j = 0; j < R[i].length; j++) {
                R[i][j] = rand.nextInt(2);
            }
        }

        print2DArray(R, "Relacja R:");

        // Sprawdzenie zwrotności
        boolean zwrotna = true;
        for (int i = 0; i < R.length; i++) {
            if (R[i][i] != 1) {
                zwrotna = false;
                break;
            }
        }
        if (zwrotna) {
            System.out.println("Ta relacja jest zwrotna!");
        } else {
            System.out.println("Ta relacja nie jest zwrotna!");
        }

        // Sprawdzenie symetrii
        int[][] R_transposed = transpose(R);

        boolean symetryczna = true;
        for (int i = 0; i < R.length; i++) {
            for (int j = 0; j < R[i].length; j++) {
                if (R[i][j] != R_transposed[i][j]) {
                    symetryczna = false;
                    break;
                }
            }
        }
        if (symetryczna) {
            System.out.println("Ta relacja jest symetryczna!");
        } else {
            System.out.println("Ta relacja nie jest symetryczna!");
        }


        // Sprawdzenie Przeciwzwrotności
        boolean przeciwZwrotna = true;
        for (int i = 0; i < R.length; i++) {
            if (R[i][i] != 0) {
                przeciwZwrotna = false;
                break;
            }
        }
        if (przeciwZwrotna) {
            System.out.println("Ta relacja jest przeciwzwrotna!");
        } else {
            System.out.println("Ta relacja nie jest przeciwzwrotna!");
        }


        // Sprawdzenie przeciwsymetrii
        boolean przeciwSymetryczna = true;
        for (int i = 0; i < R.length; i++) {
            for (int j = 0; j < R[i].length; j++) {
                if (R[i][j] == R[j][i] && i != j) {
                    przeciwSymetryczna = false;
                    i = R.length;
                    j = R.length;
                    break;
                }
            }
        }
        if (przeciwSymetryczna) {
            System.out.println("Ta relacja jest przeciwsymetryczna!");
        } else {
            System.out.println("Ta relacja nie jest przeciwsymetryczna!");
        }
    }

    private static int[][] transpose(int[][] arr) {
        int[][] arr_t = new int[arr[0].length][arr.length];
        for (int i = 0; i < arr_t.length; i++) {
            for (int j = 0; j < arr.length; j++) {
                arr_t[i][j] = arr[j][i];
            }
        }
        return arr_t;
    }

    private static void print2DArray(int[][] arr, String label) {
        System.out.println(label);
        for (int[] k : arr) {
            System.out.println(Arrays.toString(k));
        }
    }

    public static void fillWithRandom(int[] arr, int low_bound, int high_bound) {
        for (int i = 0; i < arr.length; i++) {
            arr[i] = rand.nextInt(high_bound - low_bound) + low_bound;
        }
    }
}
