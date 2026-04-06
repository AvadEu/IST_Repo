from sys import argv
import os
from os import environ, listdir, access, X_OK
from os.path import isfile, join
from typing import List

EXTENSIONS = [".exe", ".bat", ".cmd"]
PATH_SPLITTER_CHAR = ':'

def get_paths() -> List[str]:
    outcome = []
    path_var_content = environ["PATH"].split(PATH_SPLITTER_CHAR)
    for path in path_var_content:
        outcome.append(path)
    return outcome


def isExecutable(path: str, filename: str) -> bool:
    file_path = join(path, filename)
    if isfile(file_path):
        if os.name == 'posix' and os.access(file_path, os.X_OK):
            return True
        elif os.name == "Windows" and filename[-4:] in EXTENSIONS:
            return True
    else:
        return False


def main() -> None:
    if len(argv) == 1:
        print(*get_paths(), sep='\n')
    elif len(argv) == 2:
        if argv[-1] == '-x':
            for path in get_paths():
                print(path)
                try:
                    for element in listdir(path):
                        if isExecutable(path, element):
                            print(element, end=" ")
                except FileNotFoundError:
                    continue
        else:
            raise RuntimeError("Invalid argument usage")
    else:
        raise RuntimeError("Invalid usage, too many arguments")


if __name__ == "__main__":
    main()