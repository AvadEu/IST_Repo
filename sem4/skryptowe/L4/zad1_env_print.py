from os import environ
from sys import argv
from typing import List

def get_command_line_arg() -> List[tuple]:
    variables = []
    if len(argv) == 1:
        variables = list(environ.items())
    else:
        for argument in argv[1:]:
            for key, item in environ.items():
                if(argument.lower() in key.lower()):
                    variables.append((key,item))
    return variables

def main() -> None:
    variables = get_command_line_arg()
    variables.sort(key=lambda x: x[0])
    for key, item in variables:
        print(f"{key}={item}")

if __name__ == "__main__":
    main()