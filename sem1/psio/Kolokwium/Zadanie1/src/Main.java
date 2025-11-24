public class Main {
    public static void main(String[] args) {

        Obraz img1 = new Obraz();

        img1.displayImage();

        img1.displayHistogram();

        img1.displayHistogramMaxValues();

        img1.displayHistogramValuesGreaterThan(1500);
    }
}