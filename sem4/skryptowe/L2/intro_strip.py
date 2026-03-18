from utils import pprint, format_line
import sys


def intro_strip() -> str:
    line_count = 0
    consecutive_newline = 0
    buffer = ""
    afterIntro = False

    try:
        line = sys.stdin.readline()

        while line:
            cleaned = format_line(line)

            buffer += cleaned + "\n"

            if not afterIntro:
                line_count += 1
                if cleaned == "":
                    consecutive_newline += 1
                else:
                    consecutive_newline = 0

                # buffer += cleaned + "\n"

                if consecutive_newline >= 2:
                    buffer = ""
                    afterIntro = True

            line = sys.stdin.readline()
        else:
            return buffer.strip()
    except EOFError | Exception as e:
        pprint("ERROR", e)


if __name__ == "__main__":
    print(intro_strip())
