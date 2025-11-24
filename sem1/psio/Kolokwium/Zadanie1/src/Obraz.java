import java.util.Arrays;
import java.util.Random;

public class Obraz {

    final static int bound = 256;

    private int M;
    private int N;
    private int[][] bitmap;
    private int[] histogram = new int[bound];


    public Obraz() {
        this.M = 550;
        this.N = 650;
        this.bitmap = new int[M][N];
        fillWithRandoms();
        this.histogram = getHistogram();
    }

    public Obraz(int M, int N) {
        this.M = M;
        this.N = N;
        this.bitmap = new int[M][N];
        fillWithRandoms();
        this.histogram = getHistogram();
    }

    private void fillWithRandoms() {
        Random rand = new Random();
        for (int i = 0; i < M; i++) {
            for (int j = 0; j < N; j++) {
                bitmap[i][j] = rand.nextInt(0, bound);
            }
        }
    }

    public int[] getHistogram() {
        int[] LUT = new int[256];
        for (int i = 0; i < M; i++) {
            for (int j = 0; j < N; j++) {
                LUT[bitmap[i][j]]++;
            }
        }
        return LUT;
    }

    public void displayImage() {
        for (int i = 0; i < M; i++) {
            System.out.println(Arrays.toString(bitmap[i]));
        }
    }

    public void displayHistogram() {
        for (int i = 0; i < bound; i++) {
            if (histogram[i] > 0) {
                System.out.printf("%3d: %3d\n", i, histogram[i]);
            }
        }
    }

    private int getHistogramMaxValue() {
        int max = -1;
        for (int i = 0; i < bound; i++) {
            if (histogram[i] > max) {
                max = histogram[i];
            }
        }
        return max;
    }

    public void displayHistogramMaxValues() {
        int histogram_max = getHistogramMaxValue();

        System.out.println("Maksymalne wartości histogramu:");

        for (int i = 0; i < bound; i++) {
            if (histogram[i] == histogram_max) {
                System.out.print(i + " ");
            }
        }
        System.out.println();
    }

    public void displayHistogramValuesGreaterThan(int T) {
        System.out.printf("Wartości które wystąpiły więcej niż %d%n", T);

        for (int i = 0; i < bound; i++) {
            if (histogram[i] > T) {
                System.out.print(i + " ");
            }
        }
    }

}
