from typing import List, Tuple, Dict, Any
from parser import read_log
from utils import is_valid_ip, extract_extension
from datetime import datetime


def sort_log(log : List[Tuple], index : int) -> List[Tuple]:
    if 0 <= index < len(log[0]):
        return log.sort(key=(lambda x: x[index]))
    else:
        raise ValueError("Index out of bound, provide correct field index!!!")


def get_entries_by_code(log : List[Tuple], code : int) -> List[Tuple]:
    return list(filter((lambda x: x[9] == code), log))


def get_entries_by_addr(log : List[Tuple], addr : str) -> List[Tuple]:
    is_ip_valid = is_valid_ip(addr)
    if is_ip_valid:
        return list(filter((lambda x: x[2] == addr or x[7] == addr), log))
    raise ValueError("Provide a correct ip addr!")


def get_failed_reads(log: List[Tuple], merge=False) -> List[Tuple] | Tuple[List]:
    list4xx = list(filter((lambda x: (x[9] // 100 == 4) if x[9] is not None else False), log))
    list5xx = list(filter((lambda x: (x[9] // 100 == 5) if x[9] is not None else False), log))
    if merge:
        return list4xx + list5xx
    else:
        return list4xx, list5xx


def get_entries_by_extension(log: List[Tuple], ext: str) -> List[Tuple]:
    return list(filter((lambda x: extract_extension(x[8]) == ext), log))


def get_top_ips(log: List[Tuple], n=10) -> List[Tuple]:
    ip_leaderboard = {}
    for record in log:
        for addr in (record[2], record[4], record[7],):
            if not is_valid_ip(addr):
                continue
            check = ip_leaderboard.get(addr, -1)
            if check == -1:
                ip_leaderboard[addr] = 1
            else:
                ip_leaderboard[addr] += 1
    return list(sorted(ip_leaderboard.items(), key=lambda x: x[1], reverse=True)[:n])


def get_unique_methods(log: List[Tuple]) -> List[str]:
    unique_methods = set()
    for record in log:
        unique_methods.add(record[6])
    return list(unique_methods)


def get_entries_in_time_range(log: List[Tuple], start: float, end: float) -> List[Tuple]:
    start = datetime.fromtimestamp(start)
    end = datetime.fromtimestamp(end)
    return list(filter((lambda x: start <= x[0] < end) ,log))


def count_by_method(log: List[Tuple]) -> Dict[str, int]:
    keys = get_unique_methods(log)
    method_leaderboard = {method: 0 for method in keys}
    for record in log:
        method_leaderboard[record[6]] += 1
    return method_leaderboard


def get_top_uris(log: List[Tuple], n=10) -> List[str]:
    uri_leaderboard = {}
    for record in log:
        uri = record[8]        
        check = uri_leaderboard.get(uri, -1)
        if check == -1:
            uri_leaderboard[uri] = 1
        else:
            uri_leaderboard[uri] += 1
    top_uri = tuple(sorted(uri_leaderboard.items(), key=lambda x: x[1], reverse=True)[:n])
    return [k for k, _ in top_uri]


def count_status_classes(log: List[Tuple]) -> Dict[str, int]:
    status_leaderboard = {
        '2xx': 0,
        '3xx': 0,
        '4xx': 0,
        '5xx': 0
    }
    for record in log:
        if record[9] is None:
            continue
        key = str(record[9] // 100) + 'xx'
        status_leaderboard[key] += 1
    return status_leaderboard


def entry_to_dict(entry: Tuple[Any]) -> Dict[str, Any]:
    outcome = {}
    outcome['ts'] = entry[0]
    outcome['uid'] = entry[1]
    outcome['client_ip'] = entry[2]
    outcome['client_port'] = entry[3]
    outcome['server_ip'] = entry[4]
    outcome['server_port'] = entry[5]
    outcome['method'] = entry[6]
    outcome['hostname'] = entry[7]
    outcome['uri'] = entry[8]
    outcome['status'] = entry[9]
    return outcome


def log_to_dict(log: List[Tuple]) -> Dict[str, List]:
    outcome = {}
    for record in log:
        record_dict = entry_to_dict(record)
        if record_dict['uid'] in outcome.keys():
            outcome[record_dict['uid']].append(record_dict)
        else:
            outcome[record_dict['uid']] = [record_dict]
    return outcome


def print_dict_entry_dates(log_dict: Dict[str, List]) -> None:
    for k, v in log_dict.items():
        request_count = len(v)
        methods_leaderboard = {}
        status_2xx_count = 0
        print("Sesja: ", k)
        print("Liczba ządań: ", request_count)
        for entry in v:
            print("IP: ", entry['client_ip'], entry['server_ip'], entry['hostname'])
            method = entry['method']
            if method in methods_leaderboard.keys():
                methods_leaderboard[method] += 1
            else:
                methods_leaderboard[method] = 1
            if entry['status'] is not None:
                if entry['status'] // 100 == 2:
                    status_2xx_count += 1
        print("Procentowy udział metod HTTP: ")
        for method, count in methods_leaderboard.items():
            print(f'{method}: {count/request_count * 100}%')
        print(f"Udział 2xx: {status_2xx_count}/{request_count}")


def most_active_session(log_dict: Dict[str, List]) -> str:
    most_requests = 0
    outcome_uid = ''
    for k, v in log_dict.items():
        num_req = len(v)
        if num_req > most_requests:
            most_requests = num_req
            outcome_uid = k
    return outcome_uid


def get_session_paths(log: List[Tuple]) -> Dict[str, List]:
    outcome = {}
    log_dict = log_to_dict(log)
    for k, v in log_dict.items():
        list_uri = []
        for entry in v:
            list_uri.append(entry['uri'])
        outcome[k] = list_uri
    return outcome


def detect_sus(log: List[Tuple], threshold: float) -> List[str]:
    outcome = []
    ips =  get_top_ips(log, 100_000)
    for ip, count in ips:
        if count > threshold:
            outcome.append(ip)
    return outcome

if __name__ == "__main__":
    data = read_log()
    dict_data = log_to_dict(data)
    print(detect_sus(data, 3000), sep="\n")