from utils import pprint
from intro_strip import intro_strip

SENTENCE_END_CHARS = ".?!"
NUMBER_OF_SENTENCES = 20


def first_n_sentences(number_of_sentences) -> str:

    sentence_counter = 0
    text_content = intro_strip()
    sentences = text_content[0]
    for i in range(1, len(text_content)):
        previous = text_content[i-1]
        char = text_content[i]
        if previous in SENTENCE_END_CHARS:
            sentence_counter += 1
            if sentence_counter == number_of_sentences:
                return sentences
        sentences += char


if __name__ == "__main__":
    pprint(first_n_sentences(NUMBER_OF_SENTENCES))
