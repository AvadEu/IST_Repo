package Projekt_Main;

import Konto.*;
import java.util.Random;

public class Main {
    public static void main(String[] args) {
        Konto[] bank = new Konto[5];
        Random rand = new Random();

        for (int i = 0; i < bank.length; i++) {
            Waluta waluta = new Waluta(rand.nextInt(4) + 1);
            bank[i] = new Konto(waluta);
        }

        bank[0].aktywuj();
        bank[3].aktywuj();
        bank[0].dezaktywuj();

        for (int i = 0; i < bank.length; i++) {
            System.out.printf("Konto o indeksie=%d ", i);
            bank[i].getStan();
        }
    }
}
