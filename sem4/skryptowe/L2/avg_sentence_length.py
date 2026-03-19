from utils import pprint
from intro_strip import intro_strip

SENTENCE_END_CHARS = ".?!"


def avg_sentence_length() -> float:
    sentence_count = 0
    character_count = 0
    consecutive_newline = 0

    text = intro_strip()
    for char in text:
        if char.isalnum():
            character_count += 1

        if char == "\n":
            consecutive_newline += 1
        else:
            consecutive_newline = 0

        if consecutive_newline >= 2:
            sentence_count += 1

        if char in SENTENCE_END_CHARS:
            sentence_count += 1

    return character_count / sentence_count


if __name__ == "__main__":
    print("AVG: ", end="")
    pprint(str(round(avg_sentence_length(), 2)))
    pprint("\n")
