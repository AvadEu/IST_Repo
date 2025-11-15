from Utils.proces import Process
from typing import List


def round_robin(processes: List[Process], time_quantum: int):
    time = 0
    queue = processes.copy()
    completed = []

    while queue:
        current_process = queue.pop(0)

        if current_process.remaining_time <= time_quantum:
            time += current_process.remaining_time
            current_process.waiting_time = time - current_process.execution_time
            current_process.executed = True
            completed.append(current_process)
        else:
            time += time_quantum
            current_process.remaining_time -= time_quantum
            for process in queue:
                process.waiting_time += time_quantum
            queue.append(current_process)

    return completed
