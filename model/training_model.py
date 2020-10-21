from enum import Enum

import jsonpickle


class TrainingWeek:
    def __init__(self, week_start, activity_type, days):
        self.days = days
        self.activity_type = activity_type
        self.week_start = week_start
        self.week_id = f"{week_start}_{activity_type}"

    def __str__(self):
        return f"{jsonpickle.encode(self, unpicklable=False)}"


class TrainingDay:
    def __init__(self):
        self.sessions = []
        self.day = None

    def set_day(self, day):
        self.day = day

    def __str__(self) -> str:
        return f"{jsonpickle.encode(self, unpicklable=False)}"


class TrainingSession:
    def __init__(self, time, session_id, name):
        self.name = name
        self.time = time
        self.session_id = session_id

    def __str__(self) -> str:
        return f"{jsonpickle.encode(self, unpicklable=False)}"


class ActivityType(Enum):
    FREE_TRAINING = 7
