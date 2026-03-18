from utils import pprint
from intro_strip import intro_strip

SENTENCE_END_CHARS = ".?!"
WORD_END_CHARS = ";,- "


def longest_same_character() -> float:
    text_content = intro_strip()
    max_character_count = 0
    longest_sentence = ""
    character_count = 0
    sentence = ""
    previous_character_type = ""
    withoutDouble = True

    for i in range(1, len(text_content)):
        previous = text_content[i-1]
        char = text_content[i]
        character_count += 1
        sentence += char

        if previous in WORD_END_CHARS:
            if char == previous_character_type:
                withoutDouble = False
            previous_character_type = char

        if char in SENTENCE_END_CHARS:
            if character_count > max_character_count and withoutDouble:
                max_character_count = character_count
                longest_sentence = sentence
            character_count = 0
            sentence = ""
            withoutDouble = True
    return longest_sentence


if __name__ == "__main__":
    pprint(longest_same_character())
