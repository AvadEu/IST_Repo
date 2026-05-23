from typing import Callable, Iterable, Any


def forall(pred: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    return all([pred(x) for x in iterable])


def exists(pred: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    return any([pred(x) for x in iterable])


def atleast(n: int, pred: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    return sum([1 for x in iterable if pred(x)]) >= n


if __name__ == "__main__":
    arr = [1,2,3,4,5]
    print(forall(lambda x: x < 10, arr))
    print(exists(lambda x: x > 10, arr))
    print(atleast(3, lambda x: x < 4, arr))