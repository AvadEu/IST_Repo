import logging
import time
from datetime import datetime
from functools import wraps
from typing import Any, Callable, TypeVar

T = TypeVar('T')

logging.basicConfig(level=logging.DEBUG)

def _decorate_callable(func: Callable[..., Any], level: int) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger = logging.getLogger(func.__module__)
        
        call_time = datetime.now().isoformat()
        start_counter = time.perf_counter()
        
        result = func(*args, **kwargs)
        
        duration = time.perf_counter() - start_counter
        
        log_message = (
            f"Wywołanie: {call_time} | "
            f"Funkcja: {func.__qualname__} | "
            f"Argumenty: args={args}, kwargs={kwargs} | "
            f"Zwrócono: {result} | "
            f"Czas trwania: {duration:.6f}s"
        )
        
        logger.log(level, log_message)
        return result
        
    return wrapper

def log(level: int = logging.INFO) -> Callable[[T], T]:
    def decorator(target: T) -> T:
        if isinstance(target, type):
            for attr_name, attr_value in target.__dict__.items():
                if callable(attr_value):
                    setattr(target, attr_name, _decorate_callable(attr_value, level))
            return target
        elif callable(target):
            return _decorate_callable(target, level)  # type: ignore
        return target

    return decorator


if __name__ == "__main__":
    @log(level=logging.DEBUG)
    def complex_computation(x: int, y: int) -> int:
        time.sleep(0.1)
        return x * y + x

    @log(level=logging.INFO)
    class DataProcessor:
        def process_data(self, data: str) -> str:
            return data.upper()
            
        def calculate_length(self, data: str) -> int:
            return len(data)

    complex_computation(5, 10)

    processor = DataProcessor()
    processor.process_data("test")
    processor.calculate_length("test")