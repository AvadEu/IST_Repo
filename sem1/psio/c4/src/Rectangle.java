public class Rectangle {
    private Point p1;
    private Point p2;

    public Rectangle() {
        p1 = new Point(0, 0);
        p2 = new Point(1, 1);
    }

    public Rectangle(Point p1, Point p2) {
        this();
        this.ValidatePoints(p1, p2);
    }

    private void ValidatePoints(Point p1, Point p2) {
        if (p1.getX() != p2.getX() && p1.getY() != p2.getY()) {
            this.p1 = p1;
            this.p2 = p2;
        }
    }

    public double getSide1() {
        return Math.abs(this.p1.getX() - this.p2.getX());
    }

    public double getSide2() {
        return Math.abs(this.p1.getY() - this.p2.getY());
    }

    public double Diagonal() {
         return Math.sqrt(Math.pow(this.getSide1(), 2) + Math.pow(this.getSide2(), 2));
    }

    public double Area() {
        return this.getSide1() * this.getSide2();
    }

    public double Circuit() {
        return 2 * getSide1() + 2 * getSide2();
    }
}
