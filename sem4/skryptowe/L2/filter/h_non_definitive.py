from utils import pprint
from intro_strip import intro_strip


def non_definitive() -> str:
    final_outcome = ""
    text = intro_strip()

    current_sentence = ""
    for char in text:
        current_sentence += char
        if char in "?!":
            final_outcome += current_sentence + "\n"
            current_sentence = ""
        elif char == ".":
            current_sentence = ""

    return final_outcome


if __name__ == "__main__":
    pprint(non_definitive())
