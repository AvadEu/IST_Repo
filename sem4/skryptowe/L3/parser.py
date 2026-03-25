import sys
from typing import List, Tuple
from datetime import datetime

def read_log() -> List[Tuple]:
    data = []
    input_data = sys.stdin.readlines()
    input_data = [line.strip() for line in input_data]
    for line in input_data:
        splitted_line = line.split("\t")
        ts = datetime.fromtimestamp(float(splitted_line[0]))
        uid = splitted_line[1]
        client_ip = splitted_line[2]
        client_port = int(splitted_line[3])
        server_ip = splitted_line[4]
        server_port = int(splitted_line[5])
        method = splitted_line[7]
        hostname = splitted_line[8]
        uri = splitted_line[9]
        status = int(splitted_line[14]) if splitted_line[14] != "-" else None
        record = (ts, uid, client_ip, client_port, server_ip, server_port, method, hostname, uri, status,)
        data.append(record)
    return data




if __name__ == "__main__":
    pass