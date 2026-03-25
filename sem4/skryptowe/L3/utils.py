import re

def is_valid_ip(addr: str) -> bool:
    is_valid = True
    ip_splitted = addr.split(".")
    if len(ip_splitted) != 4:
        is_valid = False
    else:
        for octet in ip_splitted:
            try:
                octet = int(octet)
                if  not (0 <= octet <= 255):
                    is_valid = False
            except ValueError:
                is_valid = False
    return is_valid


def extract_extension(uri: str) -> str:
    outcome = re.findall('\\.([a-zA-Z0-9]+)(?=($|\\?|#))', uri)
    if outcome:
        return outcome[0][0]
    else:
        return "default"


if __name__ == "__main__":
    pass