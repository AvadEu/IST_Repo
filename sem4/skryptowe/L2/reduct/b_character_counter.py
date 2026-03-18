import sys
from utils import pprint


def character_counter():

    counter = 0
    for char in sys.stdin.read():
        if char.isalnum:
            counter += 1
    return counter


if __name__ == "__main__":
    pprint(str(character_counter()))
