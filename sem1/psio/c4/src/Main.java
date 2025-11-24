public class Main {
    public static void main(String[] args) {
        Rectangle r1 = new Rectangle();

        Point p1 = new Point(6, 0);
        Point p2 = new Point(0, 0);
        Rectangle r2 = new Rectangle(p1, p2);



        System.out.println(r2.Diagonal());
        System.out.println(r2.Area());
        System.out.println(r2.Circuit());
    }
}