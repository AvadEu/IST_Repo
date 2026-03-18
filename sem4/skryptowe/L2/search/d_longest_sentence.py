from utils import pprint
from intro_strip import intro_strip

SENTENCE_END_CHARS = ".?!"


def longest_sentence() -> float:
    text_content = intro_strip()
    max_character_count = 0
    longest_sentence = ""
    character_count = 0
    sentence = ""

    for i in range(1, len(text_content)):
        char = text_content[i]
        character_count += 1
        sentence += char
        if char in SENTENCE_END_CHARS:
            if character_count > max_character_count:
                max_character_count = character_count
                longest_sentence = sentence
            character_count = 0
            sentence = ""

    return longest_sentence


if __name__ == "__main__":
    pprint(longest_sentence())
