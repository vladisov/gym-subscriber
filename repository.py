import json

import boto3


def to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


class Repository:

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def insert(self, weeks):
        weeks_table = self.dynamodb.Table('weeks')
        for week in weeks:
            item = to_dict(week)
            weeks_table.put_item(Item=item)

    def find_class_by_id(self, week_start, activity_type, day, session_type, start_time):
        weeks_table = self.dynamodb.Table('weeks')
        response = weeks_table.get_item(Key={
            'week_id': f"{week_start}_{activity_type}",
        })
        # todo, efficiency, make dict
        if "Item" in response:
            week = response["Item"]
            for weekday in week["days"]:
                if weekday["day"] == day:
                    sessions = weekday["sessions"]
                    for session in sessions:
                        if session["time"] == start_time and session["name"] == session_type:
                            return session["session_id"]
        return None
