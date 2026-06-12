from functools import wraps

def repeat(n=2):
    def real_repeat(func):
        @wraps(func)
        def wrapper_repeat():
            for _ in range(n):
                func()
        return wrapper_repeat
    return real_repeat



@repeat(5)
def welcome():
    print("Hello")


welcome()