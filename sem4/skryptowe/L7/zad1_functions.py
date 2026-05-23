from typing import List, Union, Dict, Any


def acronym(words: List[str]) -> str:
    return "".join([word[0].upper() for word in words if word])


def median(numbers: List[Union[int, float]]) -> Union[int, float]:
    return (
        sorted(numbers)[len(numbers) // 2] 
        if len(numbers) % 2 != 0 
        else (sorted(numbers)[len(numbers) // 2 - 1] + sorted(numbers)[len(numbers) // 2]) / 2.0
    )


def pierwiastek(x: float, epsilon: float, y_guess: float = 1.0) -> float:
    return (
        y_guess 
        if abs(y_guess**2 - x) < epsilon 
        else pierwiastek(x, epsilon, (y_guess + x / y_guess) / 2.0)
    )


def make_alpha_dict(text: str) -> Dict[str, List[str]]:
    return {
        char: [word for word in text.split() if char in word]
        for char in set(text.replace(" ", "")) if char.isalpha()
    }


def flatten(items: List[Any]) -> List[Any]:
    return [
        element 
        for item in items 
        for element in (flatten(item) if isinstance(item, (list, tuple)) else [item])
    ]


def group_anagrams(words: List[str]) -> Dict[str, List[str]]:
    return {
        "".join(sorted(word)): [w for w in words if sorted(w) == sorted(word)]
        for word in words
    }


if __name__ == "__main__":
    print(acronym(['Zakład', 'Ubezpieczeń', 'Społecznych']))
    print(median([1,1,19,2,3,4,4,5,1]))
    print(pierwiastek(3, epsilon = 0.1))
    print(make_alpha_dict('on i ona'))
    print(flatten([1, [2, 3], [[4, 5], 6]]))
    print(group_anagrams(["kot", "tok", "pies", "kep", "pek"]))