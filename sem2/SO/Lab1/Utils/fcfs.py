from typing import List, Union
from Utils.proces import Process
import random


def fcfs(income_process_que: List[Process], random_process: Union[float, None]) -> List[Process]:
    processes = income_process_que.copy()
    time = 0
    generated = 0
    for process in processes:
        if random_process and random.random() < random_process:
            processes.append(Process(random.randint(1, 10_000), random.randint(10, 250)))
            generated += 1
        process.waiting_time = time
        time += process.execution_time
        process.executed = True
    print(f"Liczba dynamicznie dodanych procesów: {generated}")
    return processes
