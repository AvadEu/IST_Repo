import sys
from utils import pprint


def first_complex_sentence() -> str:
    current_sentence = ""
    comma_count = 0
    consecutive_newlines = 0
    prev_space = False

    try:
        char = sys.stdin.read(1)

        while char:
            if char == '\n':
                consecutive_newlines += 1
            elif not char.isspace():
                consecutive_newlines = 0

            if char.isspace():
                if current_sentence != "" and not prev_space:
                    current_sentence += " "
                    prev_space = True
            else:
                current_sentence += char
                prev_space = False

            if char == ',':
                comma_count += 1

            if char in ".!?" or consecutive_newlines >= 2:
                if current_sentence.strip() != "":
                    if comma_count > 1:
                        return current_sentence.strip() + "\n"

                    current_sentence = ""
                    comma_count = 0
                    prev_space = False

            char = sys.stdin.read(1)

    except Exception as e:
        pprint("ERROR", e)


if __name__ == "__main__":
    pprint(first_complex_sentence())
