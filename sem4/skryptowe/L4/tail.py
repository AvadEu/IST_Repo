from sys import argv, stdin
from typing import List
from pathlib import Path


def tail(file_name: str, lines: int) -> List[str]:
    if file_name != "":
        file = open(file_name)
        data = file.read()
        file.close()
    else:
        data = stdin.read()
    file_lines = data.split("\n")
    if lines < len(file_lines):
        return file_lines[-lines::]
    else:
        return file_lines


def process_command_line() -> tuple[str, int]:
    lines = 10
    file_index = argv.index(Path(__file__).name)
    input_index = file_index + 1
    if len(argv) > file_index + 1:
        if argv[file_index+1].startswith("--lines="):
            parametr = argv[file_index+1].split("=", 1)[1]
            if parametr.isnumeric():
                lines = int(parametr)
                input_index += 1
    if len(argv) >= input_index + 1:
        return argv[input_index], lines
    else:
        return "", lines
    


if __name__ == "__main__":
    tail_lines = tail(*process_command_line())
    for line in tail_lines:
        print(line)