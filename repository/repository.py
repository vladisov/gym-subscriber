import boto3

from utils.data_utils import to_dict


class Repository:
    def __init__(self):
        self.__dynamodb = boto3.resource('dynamodb')

    def insert(self, weeks):
        weeks_table = self.__dynamodb.Table('weeks')
        for week in weeks:
            item = to_dict(week)
            weeks_table.put_item(Item=item)

    def find_class_id(self, week_start, activity_type, day, session_type, start_time):
        weeks_table = self.__dynamodb.Table('weeks')
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

    def find_all(self, week_start, activity_type):
        weeks_table = self.__dynamodb.Table('weeks')
        response = weeks_table.get_item(Key={
            'week_id': f"{week_start}_{activity_type}",
        })
        # todo, efficiency, make dict
        if "Item" in response:
            week = response["Item"]
            return week
        return None
