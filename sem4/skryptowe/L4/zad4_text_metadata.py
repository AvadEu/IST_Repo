import re
import sys
from typing import List, Tuple
from collections import Counter


def load_file_content(path: str) -> List[str]:
    try:
        with open(path, 'r') as file:
            data = file.readlines()
            data = [line.strip() for line in data]
            return data
    except FileNotFoundError as e:
        sys.stderr.write(f"Given file cannot be open {e}")


def count_chars(data: List[str]) -> int:
    char_num = 0
    for line in data:
        char_num += len(line)
    return char_num


def count_words(data: List[str]) -> int:
    words_num = 0
    for line in data:
        words_num += len(line.split(" "))
    return words_num


def count_lines(data: List[str]) -> int:
    return len(data)


def most_common_char(data: List[str], num_oc=False) -> str | int:
    text = "".join(data)
    counter = Counter(text)
    if ' ' in counter:
        del counter[' ']
    most_common = counter.most_common(1)[0]
    return (most_common[1] if num_oc else most_common[0]) 



def most_common_word(data: List[str], num_oc=False) -> str | int:
    text = "".join(data)
    words = re.findall(r'\b\w+\b', text.lower())
    
    counter = Counter(words)
    most_common = counter.most_common(1)[0]
    return (most_common[1] if num_oc else most_common[0]) 


def display_csv() -> None:
    data = load_file_content(input())
    print("NumChars,NumWords,NumLines,MCChar,MCCharNum,MCWord,MCWordNum")
    print(count_chars(data),
            count_words(data),
            count_lines(data),
            most_common_char(data),
            most_common_char(data, num_oc=True),
            most_common_word(data),
            most_common_word(data, num_oc=True),
            sep=","
        )

if __name__ == "__main__":
    display_csv()
