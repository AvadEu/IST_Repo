from sys import argv, stdin
from typing import List
from pathlib import Path
import time
import os

DEFAULT_DISPLAY_MODE = 'lines'

def tail(file_name: str, lines: int) -> List[str]:
    reverse_tail = False
    if "TAIL_REVERSE" in os.environ.keys():
        if os.environ['TAIL_REVERSE'] == '1':
            reverse_tail = True

    display_mode = DEFAULT_DISPLAY_MODE
    if os.environ.get('TAIL_MODE', '') == 'chars':
        display_mode = os.environ['TAIL_MODE']

    if file_name != "":
        file = open(file_name)
        data = file.read()
        file.close()
    else:
        data = stdin.read()
    if display_mode == 'chars':
        output = data[-lines:]
        return [output]
    file_lines = data.split("\n")
    if lines < len(file_lines):
        output = file_lines[-lines::]
    else:
        output = file_lines
    if reverse_tail:
        return list(reversed(output))
    else:
        return output


def process_command_line() -> tuple[str, int, bool]:
    follow = False
    if "--follow" in argv:
        follow = True
        argv.remove("--follow")

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
        return argv[input_index], lines, follow
    else:
        return "", lines, follow


def main():
    file_name, lines_count, follow_flag = process_command_line()
    
    tail_lines = tail(file_name, lines_count)
    for line in tail_lines:
        print(line)

    if follow_flag and file_name != "":
        try:
            f = open(file_name, "r")
            f.seek(0, 2)
            
            while True:
                new_line = f.readline()
                if new_line:
                    print(new_line, end="") 
                else:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            f.close()

if __name__ == "__main__":
    main()
