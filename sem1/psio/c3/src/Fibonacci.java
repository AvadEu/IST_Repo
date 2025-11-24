public class Fibonacci {
    public static void main(String[] args) {
        int n = 6;
        int a = 0, b = 1, tmp;

        for (int i = 0; i < n; i++) {
            System.out.print(a + " ");
            tmp = a;
            a = b;
            b = b + tmp;
        }
    }
}
