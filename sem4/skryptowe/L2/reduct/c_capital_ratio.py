from utils import pprint
from intro_strip import intro_strip

SENTENCE_END_CHARS = ".?!"


def capital_ratio() -> float:
    text_content = intro_strip()

    total_sentences = 0
    sentences_with_proper_nouns = 0

    is_first_word = True
    current_proper_noun = False
    in_word = False
    current_word_capital = False

    words_in_sentence = 0
    consecutive_newlines = 0

    for char in text_content:
        if char == "\n":
            consecutive_newlines += 1
        elif not char.isspace():
            consecutive_newlines = 0

        if char.isalpha():
            if not in_word:
                in_word = True
                words_in_sentence += 1
                current_word_capital = char.isupper()
        else:
            if in_word:
                in_word = False
                if current_word_capital and not is_first_word:
                    current_proper_noun = True

                is_first_word = False

        if char in SENTENCE_END_CHARS or consecutive_newlines >= 2:
            if words_in_sentence > 0:
                total_sentences += 1
                if current_proper_noun:
                    sentences_with_proper_nouns += 1

            is_first_word = True
            current_proper_noun = False
            words_in_sentence = 0

    if words_in_sentence > 0:
        total_sentences += 1
        if current_proper_noun:
            sentences_with_proper_nouns += 1

    if total_sentences == 0:
        return 0.0

    return (sentences_with_proper_nouns / total_sentences) * 100.0


if __name__ == "__main__":
    pprint(f"{capital_ratio():.2f}%")
