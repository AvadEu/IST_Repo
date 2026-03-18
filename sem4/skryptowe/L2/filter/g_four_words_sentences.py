import sys
from utils import pprint


def four_word_sentences(output_function):
    current_sentence = ""
    word_count = 0
    in_word = False
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

            if char.isalpha():
                if not in_word:
                    word_count += 1
                    in_word = True
            else:
                in_word = False

            if char in ".!?" or consecutive_newlines >= 2:
                clean_sentence = current_sentence.strip()

                if clean_sentence != "":
                    if 0 < word_count <= 4:
                        output_function(clean_sentence + "\n")

                    current_sentence = ""
                    word_count = 0
                    in_word = False
                    prev_space = False

            char = sys.stdin.read(1)

        clean_sentence = current_sentence.strip()
        if clean_sentence != "" and 0 < word_count <= 4:
            output_function(clean_sentence + "\n")

    except Exception as e:
        output_function("ERROR", e)


if __name__ == "__main__":
    four_word_sentences(pprint)
