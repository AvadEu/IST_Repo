public class Nawiasy {
    public static boolean nawiasyZrownowazone(String wyrazenie) {
        if (wyrazenie == null || wyrazenie.isEmpty()) {
            return true;
        }

        ArrayStack<Character> stos = new ArrayStack<>(wyrazenie.length());

        for (int i = 0; i < wyrazenie.length(); i++) {
            char znak = wyrazenie.charAt(i);

            if (nawiasOtwierajacy(znak)) {
                stos.push(znak);
            } else if (nawiasZamykajacy(znak)) {
                if (stos.isEmpty()) {
                    return false;
                }

                char nawiasZeStosu = stos.pop();
                if (!pasujaceNawiasy(nawiasZeStosu, znak)) {
                    return false;
                }
            }
        }

        return stos.isEmpty();
    }

    public static boolean nawiasOtwierajacy(char ch) {
        return ch == '(' || ch == '{' || ch == '[';
    }

    public static boolean nawiasZamykajacy(char ch) {
        return ch == ')' || ch == '}' || ch == ']';
    }

    private static boolean pasujaceNawiasy(char otwierajacy, char zamykajacy) {
        return (otwierajacy == '(' && zamykajacy == ')') ||
                (otwierajacy == '{' && zamykajacy == '}') ||
                (otwierajacy == '[' && zamykajacy == ']');
    }
}
