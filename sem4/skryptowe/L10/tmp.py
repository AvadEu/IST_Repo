def once(func):
    setattr(func, "called", False)

    def wrapper():
        if not getattr(func, "called"):
            setattr(func, "called", True)
            func()
    return wrapper


@once
def hello():
    print("Hello")


if __name__ == "__main__":
    hello()
    hello()
    hello()
