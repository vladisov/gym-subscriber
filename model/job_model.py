from enum import Enum

import jsonpickle


class Job:
    def __init__(self, job_id, status):
        self.job_id = job_id
        self.status = status

    def __str__(self) -> str:
        return f"{jsonpickle.encode(self, unpicklable=False)}"


class JobRequest:

    def __init__(self, job_id, job_process, *args):
        self.job_id = job_id
        self.job_process = job_process
        self.args = args

    def __str__(self) -> str:
        return f"{jsonpickle.encode(self, unpicklable=False)}"


class JobStatus(Enum):
    RUNNING = 0,
    CANCELLED = 1
