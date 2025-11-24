import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Autosalon autosalon = new Autosalon(15);

        Scanner scanner = new Scanner(System.in);

        autosalon.getAuta();

//        int marka = scanner.nextInt();
//        autosalon.getMarkowe(marka);

//        System.out.println(autosalon.getCountAllBelow2000());
//        System.out.println(autosalon.getMostExpensive());


        System.out.println();
        autosalon.modifyPrice(0);
        autosalon.getAuta();

    }
}
