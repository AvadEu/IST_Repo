public class Tests {
    public static void runTests() {
        testAngelDecoration();
        testBaubleDecoration();
        testInvalidDecorationThrowsException();
        testTreeHeightValidation();
    }

    private static void testAngelDecoration() {
        System.out.print("Test 1 (Aniołek): ");
        ChristmasTree tree = new PineTree(3);
        IDecoration angel = new AngelDecoration();
        tree.applyDecoration(angel);

        String topRow = tree.getRepresentation().get(0).toString();
        if (topRow.contains("A")) {
            System.out.println("PASSED");
        } else {
            System.out.println("FAILED (Brak aniołka na szczycie)");
        }
    }

    private static void testBaubleDecoration() {
        System.out.print("Test 2 (Bombki): ");
        ChristmasTree tree = new PineTree(3);
        IDecoration baubles = new BaubleDecoration();
        tree.applyDecoration(baubles);

        String fullTree = tree.toString();
        if (fullTree.contains("o")) {
            System.out.println("PASSED");
        } else {
            System.out.println("FAILED (Brak bombek)");
        }
    }

    private static void testInvalidDecorationThrowsException() {
        System.out.print("Test 3 (Błędna nazwa): ");
        DecorationFactory factory = new DecorationFactory();
        try {
            factory.getDecoration("samochód");
            System.out.println("FAILED (Nie rzucono wyjątku)");
        } catch (InvalidDecorationException e) {
            System.out.println("PASSED (Złapano wyjątek: " + e.getMessage() + ")");
        }
    }

    private static void testTreeHeightValidation() {
        System.out.print("Test 4 (Wysokość < 2): ");
        try {
            new PineTree(1);
            System.out.println("FAILED (Pozwolono na zbyt małe drzewo)");
        } catch (IllegalArgumentException e) {
            System.out.println("PASSED");
        }
    }
}

