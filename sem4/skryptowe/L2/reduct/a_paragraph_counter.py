from utils import format_line, pprint
import sys


def paragraphCounter():

    counter = 0
    line = sys.stdin.readline()

    while line:
        line = format_line(line)
        if line == "":
            counter += 1
        line = sys.stdin.readline()
    return counter


if __name__ == "__main__":
    pprint(str(paragraphCounter()))
