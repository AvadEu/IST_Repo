public class IsPrime {
    public static void main(String[] args) {
        int n = 14;

        if (n < 2) {
            System.out.println("Liczba nie jest pierwsza!");
        } else {
            for (int i = 2; i <= Math.sqrt(n); i++) {
                if (n % i == 0) {
                    System.out.printf("Liczba %d nie jest pierwsza!", n);
                    System.exit(0);
                }
            }
            System.out.printf("Liczba %d jest pierwsza!", n);
        }
    }
}
