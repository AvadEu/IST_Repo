import java.util.Arrays;

public class BubbleSort {

    public static void main(String[] args) {
        int[] arr = {76,71, 5, 57,12,50,20,93,20,55,62,3};
        bubbleSort(arr);
    }

    private static void swap(int[] array, int i, int j) {
        int tmp = array[i];
        array[i] = array[j];
        array[j] = tmp;
    }

    private static void bubbleSort(int[] array) {
        for (int i = 0; i < array.length - 1; i++) {
            for (int j = array.length - 1; j > i; j--) {
                if (array[j] > array[j - 1]) {
                    swap(array, j, j - 1);
                    System.out.println(Arrays.toString(array));
                    System.out.println();
                }
            }
        }
    }
}