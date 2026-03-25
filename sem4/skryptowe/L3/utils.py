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
    ext_query_str = uri.split('/')[-1]
    file = ext_query_str.split('?')[0]
    ext = file.split('.')[-1]
    return ext


if __name__ == "__main__":
    pass