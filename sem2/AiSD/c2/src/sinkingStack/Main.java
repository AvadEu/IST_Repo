package sinkingStack;

import stack.EmptyStackException;

public class Main {
    public static void main(String[] args) throws EmptyStackException {
        NonOptimalSinkingStack<Integer> stack = new NonOptimalSinkingStack<>(3);
        stack.push(1);
        stack.push(2);
        stack.push(3);
        stack.push(4);
        while (!stack.isEmpty()) {

            System.out.println(stack.pop());
        }
    }
}
