from typing import Any
import sys


def pprint(text: str) -> Any:
    sys.stdout.write(text)


def format_line(line_str: str) -> str:
    stripped = line_str.strip()
    result = ""
    prev_space = False

    for char in stripped:
        if char.isspace():
            if not prev_space:
                result += " "
                prev_space = True
        else:
            result += char
            prev_space = False

    return result
