import sys
from utils import pprint


def target_words_sentences(output_function):
    current_sentence = ""
    current_word = ""
    target_words_count = 0
    consecutive_newlines = 0
    prev_space = False

    try:
        char = sys.stdin.read(1)

        while char:

            if char == '\n':
                consecutive_newlines += 1
            elif not char.isspace():
                consecutive_newlines = 0

            if char.isalpha():
                current_word += char
            else:
                if current_word != "":
                    cw_lower = current_word.lower()
                    if (cw_lower == "i" or cw_lower == "oraz" or
                        cw_lower == "ale" or cw_lower == "że" or
                            cw_lower == "lub"):
                        target_words_count += 1

                    current_word = ""

            if char.isspace():
                if current_sentence != "" and not prev_space:
                    current_sentence += " "
                    prev_space = True
            else:
                current_sentence += char
                prev_space = False

            if char in ".!?" or consecutive_newlines >= 2:
                clean_sentence = current_sentence.strip()

                if clean_sentence != "":

                    if target_words_count >= 2:
                        output_function(clean_sentence + "\n")

                    current_sentence = ""
                    target_words_count = 0
                    prev_space = False

            char = sys.stdin.read(1)

        if current_word != "":
            cw_lower = current_word.lower()
            if (cw_lower == "i" or cw_lower == "oraz" or
                    cw_lower == "ale" or cw_lower == "że" or cw_lower == "lub"):
                target_words_count += 1

        clean_sentence = current_sentence.strip()
        if clean_sentence != "" and target_words_count >= 2:
            output_function(clean_sentence + "\n")

    except Exception as e:
        output_function("ERROR", e)


if __name__ == "__main__":
    target_words_sentences(pprint)
