import java.util.Arrays;

public class Task1 {

    private static boolean isSorted(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            if (arr[i] > arr[i + 1]) return false;
        }
        return true;
    }

    public static int[] insert(int[] arr, int x) {
        if (arr == null) throw new IllegalArgumentException("Tablica nie może być nullem");
        if (!isSorted(arr)) throw new IllegalArgumentException("Tablica wejściowa musi być posortowana");

        int[] result = new int[arr.length + 1];
        int i = 0;
        int j = 0;
        boolean inserted = false;

        while (i < arr.length) {
            if (!inserted && arr[i] >= x) {
                result[j++] = x;
                inserted = true;
            } else {
                result[j++] = arr[i++];
            }
        }
        
        if (!inserted) {
            result[j] = x;
        }

        return result;
    }

    public static void main(String[] args) {
        int[] t1 = {1, 3, 5, 7};
        int[] t2 = {};
        int[] t3 = {1, 2, 3};
        int[] t4 = {-5, 0, 5};
        
        System.out.println(Arrays.toString(insert(t1, 4))); // [1, 3, 4, 5, 7]
        System.out.println(Arrays.toString(insert(t2, 5))); // [5]
        System.out.println(Arrays.toString(insert(t3, 0))); // [0, 1, 2, 3]
        System.out.println(Arrays.toString(insert(t4, 10))); // [-5, 0, 5, 10]
        
        // int[] tError = {3, 1};
        // insert(tError, 2);
    }
}