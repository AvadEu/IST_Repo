public class Main {
    public static void main(String[] args) {
        Zegar z1 = new Zegar();
        Zegar z2 = new Zegar(1, 30, 0);

        z1.Przesun(1, 15, 25);
        z2.Przesun(0,10,10);

        z1.Wypisz();
        z2.Wypisz();

        z2.Przesun(25,0,0);
        z2.Wypisz();
    }
}