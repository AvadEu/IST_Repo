from typing import Callable, Generator, Any

def make_generator(f: Callable[[int], Any]) -> Generator[Any, None, None]:
    def inner_generator() -> Generator[Any, None, None]:
        n = 1
        while True:
            yield f(n)
            n += 1
            
    return inner_generator()

def fibonacci(n: int) -> int:
    return 1 if n <= 2 else fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == "__main__":
    fib_gen = make_generator(fibonacci)

    arithmetic_gen = make_generator(lambda n: 2 + (n - 1) * 3)
    geometric_gen = make_generator(lambda n: 2 * (3 ** (n - 1)))
    power_gen = make_generator(lambda n: n ** 2)

    fib_first_5 = [next(fib_gen) for _ in range(5)]
    arithmetic_first_5 = [next(arithmetic_gen) for _ in range(5)]
    geometric_first_5 = [next(geometric_gen) for _ in range(5)]
    power_first_5 = [next(power_gen) for _ in range(5)]

    print(f"Fibonacci: {fib_first_5}")
    print(f"Arytmetyczny: {arithmetic_first_5}")
    print(f"Geometryczny: {geometric_first_5}")
    print(f"Potęgowy: {power_first_5}")