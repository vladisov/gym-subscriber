class Repository:

    def __init__(self, week_map):
        self.week_map = week_map

    def find_class_by_id(self, week_start, activity_type, day, session_type, start_time):
        week_map = self.week_map
        week_key = f"{week_start}_{activity_type}"
        if week_key in week_map:
            if day in week_map[week_key]:
                if start_time in week_map[week_key][day]:
                    sessions = week_map[week_key][day][start_time]
                    for session in sessions:
                        if session[0] == session_type:
                            return session[1]
        return None
