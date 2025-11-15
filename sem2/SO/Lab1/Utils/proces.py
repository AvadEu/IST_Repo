class Process:
    def __init__(self, pid, execution_time):
        self.pid = pid
        self.execution_time = execution_time
        self.waiting_time = 0
        self.remaining_time = execution_time
        self.executed = False
        self.last_finished = 0
