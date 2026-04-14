import sys
import json
import re

def file_processer() -> json:
    data = sys.stdin.read()
    words = re.findall(r'\w+(?:-\w+)*', data)
    chars = list(data)

    path = __file__
    char_counter = len(data)
    words_counter = len(words)
    line_counter = len(data.split("\n"))
    max_char = max(set(chars), key=chars.count)
    max_word = max(set(words), key=words.count)

    result = {
        "path": path,
        "char_counter": char_counter,
        "words_counter": words_counter,
        "line_counter": line_counter,
        "max_char": max_char,
        "max_word": max_word
    }

    return json.dumps(result, indent=3)


if __name__ == "__main__":
    print(file_processer())