public class Main {

    public static void printAll(Object... args) {
        printRecursive(args, 0);
    }

    private static void printRecursive(Object[] args, int index) {
        if (index >= args.length) {
            return;
        }

        Object obj = args[index];
        String typeName = (obj != null) ? obj.getClass().getSimpleName() : "Null";

        System.out.println(typeName + ": " + obj);

        printRecursive(args, index + 1);
    }

    public static void main(String[] args) {
        printAll(1, "hello", 3.14);

        printAll('c', 100, 999999999L);

        printAll(new java.util.Date(), new java.util.ArrayList<>());

        printAll("Just String");
    }
}