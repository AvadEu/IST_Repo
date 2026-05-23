import random
import string
from typing import Iterator

class PasswordGenerator:
    def __init__(
        self, 
        length: int, 
        count: int, 
        charset: str = string.ascii_letters + string.digits
    ) -> None:
        self.length = length
        self.charset = charset
        self.count = count
        self._generated_count = 0

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        if self._generated_count >= self.count:
            raise StopIteration
        
        self._generated_count += 1
        return "".join(random.choices(self.charset, k=self.length))


if __name__ == "__main__":
    generator = PasswordGenerator(length=12, count=4)
    print(next(generator))
    for password in generator:
        print(password)