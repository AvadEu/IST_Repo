package Obserwator;

import Obserwator.Inwestorzy.Inwestor;
import Obserwator.Podmioty.Stock;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Inwestor Marek = new Inwestor("Marek Nowak", 43, 500.00, "Polska");
        Inwestor John = new Inwestor("John Smith", 70, 10000.00, "USA");

        Stock firma1 = new Stock("Inpost sp. z.o.o", 100.00);

        firma1.registerObserver(Marek);
        firma1.registerObserver(John);

        System.out.println(Marek.toString());
        System.out.println(John.toString());

        Scanner sc = new Scanner(System.in);

        while (true) {
            System.out.println("1 - zmień cenę");
            System.out.println("2 - zakończ");

            int choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                    System.out.println("Podaj cenę: ");
                    double cena = sc.nextDouble();
                    firma1.priceChange(cena);
                    break;
                case 2:
                    System.exit(0);
                    break;
                default:
                    System.out.println("Wybrano nie poprawną opcję!");
            }
        }
    }
}
