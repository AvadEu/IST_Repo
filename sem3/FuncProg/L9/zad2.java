import java.util.Arrays;

public class Task2 {

    public static int[] removeDuplicates(int[] arr, int target) {
        if (arr == null) throw new IllegalArgumentException("Tablica nie może być pusta");

        int count = 0;
        for (int val : arr) {
            if (val == target) count++;
        }

        if (count <= 1) {
            return Arrays.copyOf(arr, arr.length);
        }

        int newSize = arr.length - (count - 1);
        int[] result = new int[newSize];
        
        int destIndex = 0;
        boolean foundFirst = false;

        for (int val : arr) {
            if (val == target) {
                if (!foundFirst) {
                    result[destIndex++] = val;
                    foundFirst = true;
                }
            } else {
                result[destIndex++] = val;
            }
        }

        return result;
    }

    public static void main(String[] args) {
        int[] t1 = {1, 2, 2, 2, 3, 1, 4, 2};
        int[] t2 = {5, 5, 5};
        int[] t3 = {1, 2, 3};
        int[] t4 = {};
        int[] t5 = {2, 1, 2, 1}; // target 2 -> oczekiwane {2, 1, 1}

        System.out.println("Test 1: " + Arrays.toString(removeDuplicates(t1, 2))); // [1, 2, 3, 1, 4]
        System.out.println("Test 2: " + Arrays.toString(removeDuplicates(t2, 5))); // [5]
        System.out.println("Test 3: " + Arrays.toString(removeDuplicates(t3, 4))); // [1, 2, 3]
        System.out.println("Test 4: " + Arrays.toString(removeDuplicates(t4, 1))); // []
        System.out.println("Test 5: " + Arrays.toString(removeDuplicates(t5, 2))); // [2, 1, 1]
    }
}