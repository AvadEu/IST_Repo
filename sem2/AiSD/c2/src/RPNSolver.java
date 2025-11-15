import queue.EmptyQueueException;
import queue.IQueue;
import stack.ArrayStack;
import stack.EmptyStackException;
import stack.FullStackException;

public class RPNSolver {

    public static double evaluateRPN(IQueue<String> queue) throws EmptyQueueException, EmptyStackException, FullStackException {

        ArrayStack<Double> stack = new ArrayStack<>();

        while (!queue.isEmpty()) {
            String token = queue.dequeue();
            if (isOperator(token)) {
                double b = stack.pop();
                double a = stack.pop();
                stack.push(applyOperator(token, a, b));
            } else {
                stack.push(Double.parseDouble(token.toString()));
            }
        }
        return stack.pop();
    }

    private static boolean isOperator(Object token) {
        return token.equals("+") || token.equals("-") ||
                token.equals("*") || token.equals("/") ||
                token.equals("%");
    }

    private static double applyOperator(String operator, double a, double b) {
        switch (operator) {
            case "+":
                return a + b;
            case "-":
                return a - b;
            case "*":
                return a * b;
            case "/":
                return a / b;
            case "%":
                return a % b;
            default:
                throw new IllegalArgumentException("Nieprawidłowy operator: " + operator);
        }
    }
}
