public class Student {
    private int album;
    private double srednia_ocen;

    public Student() {
        this.album = 0;
        this.srednia_ocen = 0;
    }

    public Student(int album, double srednia_ocen) {
        this.album = album;
        this.srednia_ocen = srednia_ocen;
    }

    public int getAlbum() {
        return this.album;
    }

    public void setAlbum(int album) {
        this.album = album;
    }

    public double getSrednia_ocen() {
        return this.srednia_ocen;
    }

    public void setSrednia_ocen(double srednia_ocen) {
        this.srednia_ocen = srednia_ocen;
    }

    public void getStan() {
        System.out.printf("album=%3d, średnia=%4.2f\n", album, srednia_ocen);
    }
}
