public class Zadanie1 {
    public static void main(String[] args) {
        int n = 10;

        if (n < 0) {
            System.out.println("Nie spełnia założenia!");
        } else {
            double l = -2;
            double m = 2;
            String ls = "" + l;
            String ms = "" + m;

            int i = 1;
            while (i < n) {
                double tmp1 = (3 * i +2);
                ms = ms + " " + tmp1;
                m = m * tmp1;

                double tmp2 = 5 * i;
                if (i % 2 == 0) {
                    tmp2 = tmp2 * -1;
                }
                tmp2 = tmp2 + (Math.pow(-1, i) * -2);
                l = l + tmp2;
                ls = ls + " " + tmp2;

                i++;
            }

            double p = l / m;
            System.out.println(l);
            System.out.println(m);
            System.out.printf("%s %n %s %n", ls, ms);
            System.out.println(p);
        }
    }
}
