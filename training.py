from enum import Enum


class TrainingWeek:
    def __init__(self, activity_type):
        self.days = []
        self.activity_type = activity_type
        self.week_start = None

    def set_week_start(self, week_start):
        self.week_start = week_start


class TrainingDay:
    def __init__(self):
        self.sessions = []
        self.day = None

    def set_day(self, day):
        self.day = day

    def __str__(self) -> str:
        return f"{self.day} - {self.sessions}"


class TrainingSession:
    def __init__(self, time, session_id, name):
        self.name = name
        self.time = time
        self.session_id = session_id

    def __str__(self) -> str:
        return f"{self.name} - {self.time} - {self.session_id}"


class ActivityType(Enum):
    FREE_TRAINING = 7
