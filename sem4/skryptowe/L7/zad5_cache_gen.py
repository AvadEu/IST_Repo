from typing import Callable, Generator, Any
from functools import cache

def make_generator(f: Callable[[int], Any]) -> Generator[Any, None, None]:
    def inner_generator() -> Generator[Any, None, None]:
        n = 1
        while True:
            yield f(n)
            n += 1
    return inner_generator()

def make_generator_mem(f: Callable[[int], Any]) -> Generator[Any, None, None]:
    return make_generator(cache(f))

@cache
def fibonacci(n: int) -> int:
    return 1 if n <= 2 else fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == "__main__":
    fib_gen_mem = make_generator_mem(fibonacci)

    fib_first_10 = [next(fib_gen_mem) for _ in range(10)]
    print(f"Fibonacci (memoizacja): {fib_first_10}")