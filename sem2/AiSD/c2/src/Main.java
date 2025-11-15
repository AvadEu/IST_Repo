import queue.IQueue;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) throws Exception{
        Scanner scanner = new Scanner(System.in);

        System.out.println("Podaj wyrażenie: ");
        String expression = scanner.nextLine();

        if (expression.length() == 0) {
            System.out.println("Pusta formuła");
            return;
        }

        System.out.println("Wyrażenie " + expression + " w RPN:");
        IQueue<String> queue = MyAnalyzer.analize(expression);
        System.out.println(MyAnalyzer.toRPNString(queue));

        System.out.println("Wynik: " + RPNSolver.evaluateRPN(queue));

    }
}