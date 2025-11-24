public class Zad1 {
    public static void main(String[] args) {
        int[] a = {1, 1, 2, 2, 3};
        int[] b = {5, 2};

        a = filterDuplicates(a, 3);
        b = filterDuplicates(b, 5);

        intersection(a, b);
        System.out.println();
        difference(a, b);

    }

    public static void intersection(int[] arr1,int[] arr2) {


        for (int i = 0; i < Math.max(arr1.length, arr2.length); i++) {
            for (int j = 0; j < Math.min(arr1.length, arr2.length); j++) {
                if (arr1[i] == arr2[j]) {
                    System.out.print(arr1[i] + " ");
                }
            }
        }
    }

    public static void difference(int[] arr1,int[] arr2) {

        for (int i = 0; i < Math.max(arr1.length, arr2.length); i++) {
        boolean found = false;
            for (int j = 0; j < Math.min(arr1.length, arr2.length); j++) {
                if (arr1[i] == arr2[j]) {
                    found = true;
                }
            }
            if (!found) {
                System.out.print(arr1[i] + " ");
            }
        }
    }

    public static int[] filterDuplicates(int[] arr, int hb) {
        int[] filtered = new int[arr.length];
        int[] lut = new int[hb + 1];

        for (int i = 0; i < arr.length; i++) {
            lut[arr[i]]++;
        }

        int j = 0;
        for (int i = 0; i < lut.length; i++) {
            if (lut[i] > 0) {
                filtered[j] = i;
                j++;
            }
        }
        int[] outcome = new int[j];
        for (int i = 0; i < j; i++) {
            outcome[i] = filtered[i];
        }

        return outcome;
    }
}
