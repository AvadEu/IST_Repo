import java.util.Arrays;
import java.util.Random;

public class Main {
    public static void main(String[] args) {
        final int SIZE = 25000;
        final int BOUND = 100000;

        System.out.println("Czas sortowania [dane losowe] [dane rosnące] [dane malejące]");
        for (int i = 0; i < 10; i++) {
                int[] randomArr = generateRandomArray(SIZE, BOUND);
                int[] randomAsc = Arrays.copyOf(randomArr, SIZE);
                Arrays.sort(randomAsc);
                int[] randomDesc = Arrays.copyOf(randomAsc, SIZE);
                reverseArray(randomDesc);
                long startRandom = System.nanoTime();
//                Algorithms.bubbleSort(randomArr);
//                Algorithms.selectSort(randomAsc);
//                Algorithms.insertSort(randomDesc);
                Algorithms.quickSort(randomArr, 0, randomArr.length - 1);
//                Algorithms.mergeSort(randomAsc, 0, randomAsc.length - 1);
//                Algorithms.heapSort(randomDesc);
                long timeRandom = System.nanoTime() - startRandom;

                long startAsc = System.nanoTime();
//                Algorithms.bubbleSort(randomAsc);
//                Algorithms.selectSort(randomAsc);
//                Algorithms.insertSort(randomDesc);
                Algorithms.quickSort(randomArr, 0, randomArr.length - 1);
//                Algorithms.mergeSort(randomAsc, 0, randomAsc.length - 1);
//                Algorithms.heapSort(randomDesc);
                long timeAsc = System.nanoTime() - startAsc;

                long startDesc = System.nanoTime();
//                Algorithms.bubbleSort(randomDesc);
//                Algorithms.selectSort(randomAsc);
//                Algorithms.insertSort(randomDesc);
                Algorithms.quickSort(randomArr, 0, randomArr.length - 1);
//                Algorithms.mergeSort(randomAsc, 0, randomAsc.length - 1);
//                Algorithms.heapSort(randomDesc);
                long timeDesc = System.nanoTime() - startDesc;
                System.out.print(timeRandom + " ");
                System.out.print(timeAsc + " ");
                System.out.print(timeDesc + " ");
                System.out.println();

        }
    }

    public static int[] generateRandomArray(int size, int bound) {
        Random rand = new Random();
        int[] arr = new int[size];
        for (int i = 0; i < size; i++) {
            arr[i] = rand.nextInt(bound);
        }
        return arr;
    }

    public static void reverseArray(int[] arr) {
        int left = 0, right = arr.length - 1;
        while (left < right) {
            int temp = arr[left];
            arr[left] = arr[right];
            arr[right] = temp;
            left++;
            right--;
        }
    }
}