import java.util.*;

public class ONPConverter {

    private static boolean isOperator(char c) {
        return c == '+' || c == '-' || c == '*' || c == '/' || c == '%';
    }

    private static int precedence(char op) {
        return switch (op) {
            case '+', '-' -> 1;
            case '*', '/', '%' -> 2;
            default -> -1;
        };
    }

    public static List<String> toONP(String expr) {
        List<String> output = new ArrayList<>();
        Stack<Character> stack = new Stack<>();
        int i = 0;

        while (i < expr.length()) {
            char c = expr.charAt(i);

            if (Character.isWhitespace(c)) {
                i++;
                continue;
            }

            if (Character.isDigit(c)) {
                StringBuilder number = new StringBuilder();
                while (i < expr.length() && (Character.isDigit(expr.charAt(i)) || expr.charAt(i) == '.')) {
                    number.append(expr.charAt(i));
                    i++;
                }
                output.add(number.toString());
                continue;
            }

            if (c == '(') {
                stack.push(c);
            }

            else if (c == ')') {
                while (!stack.isEmpty() && stack.peek() != '(') {
                    output.add(String.valueOf(stack.pop()));
                }
                if (!stack.isEmpty() && stack.peek() == '(') {
                    stack.pop();
                }
            }

            else if (isOperator(c)) {
                while (!stack.isEmpty() && isOperator(stack.peek()) && precedence(c) <= precedence(stack.peek())) {
                    output.add(String.valueOf(stack.pop()));
                }
                stack.push(c);
            }

            i++;
        }

        while (!stack.isEmpty()) {
            output.add(String.valueOf(stack.pop()));
        }

        return output;
    }
}
