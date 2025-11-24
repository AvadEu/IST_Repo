public class Drawing {
    public static void main(String[] args) {
        int height = 4;

        if (height < 2) {
            System.out.println("Wymagane przynajmniej dwa wiersze!!");
        }

        for (int i = 1; i <= height; i++) { // Wiersze góra

            for (int j = i; j < height; j++) {
                System.out.print(" ");
            }

            for (int n = 1; n <= (2 * i - 1); n++) {
                System.out.print("*");
            }
            System.out.println();
        }

        for (int i = height - 1; i >= 0; i--) { // Wiersze dół

            for (int j = height; j > i; j--) {
                System.out.print(" ");
            }

            for (int n = 1; n <= (2 * i - 1); n++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }
}
