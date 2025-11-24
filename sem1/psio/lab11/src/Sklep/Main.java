package Sklep;

import Dostawa.DostawaKurier;
import Dostawa.DostawaOdbiór;
import Dostawa.SposóbDostawy;
import Zamówienie.*;
import Płatność.*;

import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;
import java.util.ArrayList;

public class Main {

    static ArrayList<Zamówienie> baza = new ArrayList<>();

    public static void main(String[] args) {

        Zamówienie z1 = new ZamówienieHurtowe(100.00, 0.1, false, "123");
        baza.add(z1);

        while (true) {
            displayMenu();
            Scanner scanner = new Scanner(System.in);
            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1:
                    addZamówienie();
                    break;
                case 2:
                    System.out.println("Które zamówienie chcesz z finalizować: ");
                    int n = scanner.nextInt();
                    scanner.nextLine();
                    finalizujZamówienie(n-1);
                    break;
                case 3:
                    wyświetlWszystkieZamówienia();
                    break;
                case 4:
                    eksportDoPliku();
                    break;
                case 5:
                    System.out.println("Do widzenia!");
                    System.exit(0);
                    break;
                default:
                    System.out.println("Wybrano nie poprawną opcję!");
                    break;
            }
        }
    }

    public static void displayMenu() {
        System.out.println("Witaj w systemie naszego sklepu! Wybierz opcję:");
        System.out.println("1 - Złóż zamówienie");
        System.out.println("2 - Finalizuj zamówienie");
        System.out.println("3 - Zobacz zamówienia");
        System.out.println("4 - Eksportuj zamówienia do pliku");
        System.out.println("5 - Zakończ");
    }

    public static void addZamówienie() {
        Scanner scanner = new Scanner(System.in);
        System.out.printf("Wybierz typ zamówienia:%n1 - Detaliczne%n2 - Hurtowe%n");
        int typ = scanner.nextInt();
        scanner.nextLine();
        System.out.printf("Podaj dane zamówienia:%nWartość: ");
        double value = scanner.nextDouble();
        scanner.nextLine();
        System.out.print("Zniżka: ");
        double discount = scanner.nextDouble();
        scanner.nextLine();

        switch (typ) {
            case 1:
                System.out.println("Czy zapakować na prezent");
                boolean zapakować = scanner.nextBoolean();
                scanner.nextLine();
                Zamówienie order = new ZamówienieDetaliczne(value, discount, zapakować);
                baza.add(order);
                System.out.println("Zamówienie dodano poprawnie!");
                break;
            case 2:
                System.out.println("Czy wystawić fakturę VAT: ");
                boolean fakturVat = scanner.nextBoolean();
                scanner.nextLine();
                String NIP = "-";
                if (fakturVat) {
                    System.out.println("Podaj NIP");
                    NIP = scanner.nextLine();
                }
                order = new ZamówienieHurtowe(value, discount, fakturVat, NIP);
                baza.add(order);
                break;
            default:
                System.out.println("Wybrano nie poprawnie!");
                break;
        }
    }

    public static void wyświetlWszystkieZamówienia() {
        for (int i = 0; i < baza.size(); i++) {
            if (baza.get(i).isZfinalizowane()) {
                System.out.println(baza.get(i).toString() + " -> " + baza.get(i).getPłatność().toString() + " -> " + baza.get(i).getDostawa().toString());
            } else {
                System.out.println(baza.get(i).toString());
            }
        }
    }

    public static void finalizujZamówienie(int numer) {
        try {
            Zamówienie doFinalizacji = baza.get(numer);
        }
        catch (IndexOutOfBoundsException e) {
            System.out.println("Nie poprawny numer zamówienia!");
            return;
        }

        Scanner sc = new Scanner(System.in);
        System.out.printf("Wybierz sposób płatności:%n1 - BLIK%n2 - PayPal%n3 - Przelew%n");
        int payment = sc.nextInt();
        sc.nextLine();
        SposóbPłatności p = getPłatność(payment);
        System.out.printf("Wybierz sposób dostawy:%n1 - Kurier%n2 - Odbiór osobisty%n");
        int dostawa = sc.nextInt();
        sc.nextLine();
        SposóbDostawy d = getDostawa(dostawa);
        baza.get(numer).setDostawa(d);
        baza.get(numer).finalizujZamówienie(p, d);
    }
    public static SposóbDostawy getDostawa(int rodzaj) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Podaj adres dostawy: ");
        String adres = sc.nextLine();
        switch (rodzaj) {
            case 1:
                System.out.println("Czy dostawa ma być ekspresowa: ");
                boolean ekspresowa = sc.nextBoolean();
                return new DostawaKurier(adres, ekspresowa);
            case 2:
                System.out.println("Podaj waga przesyłki: ");
                int waga = sc.nextInt();
                sc.nextLine();
                return new DostawaOdbiór(adres, waga);
            default:
                return null;
        }
    }


    public static SposóbPłatności getPłatność(int typ) {
        Scanner sc = new Scanner(System.in);
        switch (typ) {
            case 1:
                System.out.printf("Podaj numer telefonu:%n");
                String numerTelefonu = sc.nextLine();
                System.out.printf("Podaj kod BLIK:%n");
                String kodBLIK = sc.nextLine();
                return new PłatnośćBLIK(numerTelefonu, kodBLIK);
            case 2:
                System.out.printf("Podaj adres e-mail:%n");
                String adresEmail = sc.nextLine();
                return new PłatnośćPayPal(adresEmail);
            case 3:
                System.out.printf("Podaj odbiorcę:%n");
                String odbiorca = sc.nextLine();
                System.out.printf("Podaj numer IBAN:%n");
                String numerIBAN = sc.nextLine();
                return new PłatnośćPrzelew(odbiorca, numerIBAN);
            default:
                return null;
        }
    }

    public static void eksportDoPliku() {
        FileWriter fw;
        try {
            fw = new FileWriter("baza.txt");
            for (int i = 0; i < baza.size(); i++) {
                    if (baza.get(i).isZfinalizowane()) {
                        fw.write(baza.get(i).toString() + " -> " + baza.get(i).getPłatność().toString());
                    } else {
                        fw.write(baza.get(i).toString());
                    }
                }
            fw.close();
            System.out.println("Zapis udany!");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}