from Utils.proces import Process
from typing import List, Union

import random


def srtf(income_process_que: List[Process], random_process: Union[float, None]) -> List[Process]:
    processes = income_process_que.copy()
    processes.sort(key=lambda x: x.execution_time)
    time = 0
    generated = 0
    for process in processes:
        if random_process and random.random() < random_process:
            new_process = Process(random.randint(1, 10_000), random.randint(10, 45))
            generated += 1
            processes.append(process)
            process.execution_time = -1
            processes.append(new_process)
            processes.sort(key=lambda x: x.execution_time)
            continue
        if process.execution_time != -1:
            process.waiting_time = time
            time += process.execution_time
            process.executed = True
    print(f"Liczba dynamicznie dodanych procesów: {generated}")
    return processes


def sjf(income_process_que: List[Process], random_process: Union[float, None]) -> List[Process]:
    processes = income_process_que.copy()
    processes.sort(key=lambda x: x.execution_time)
    time = 0
    generated = 0
    for process in processes:
        if random_process and random.random() < random_process:
            processes.append(Process(random.randint(1, 10_000), random.randint(10, 250)))
            generated += 1
            processes.sort(key=lambda x: x.execution_time)
        process.waiting_time = time
        time += process.execution_time
        process.executed = True
    print(f"Liczba dynamicznie dodanych procesów: {generated}")
    return processes
