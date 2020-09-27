from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from authorizer import Authorizer
from parser import Parser
from repository import Repository
from subscriber import Subscriber
from training import ActivityType
from datetime import datetime
import sys


def init_driver():
    options = Options()
    options.headless = True
    return webdriver.Chrome('./chromedriver', options=options)


if __name__ == '__main__':
    base_api = "https://{0}/classes/week/{1}"
    "?event_type={2}&coach=0&activity_id=0&member_id_filter=0&embedded=0&planner_type={2}"
    "&show_personnel_schedule=0&in_app=0&single_club=0"
    email = sys.argv[1]
    password = sys.argv[2]
    gym_url = sys.argv[3]
    now = datetime.now().strftime("%Y-%m-%d")
    activity_type = ActivityType.FREE_TRAINING

    driver = init_driver()

    authorizer = Authorizer(driver, base_api)
    driver = authorizer.authorize(now, gym_url, activity_type, email, password)

    # parses three weeks
    parser = Parser(driver, now, activity_type)
    weeks = parser.parse(3)

    week_map = {}
    for week in weeks:
        week_key = f"{week.week_start}_{week.activity_type.name}"
        week_map[week_key] = {}
        day_week_map = {}
        for week_day in week.days:
            day_str = week_day.day
            session_map = {}
            for session in week_day.sessions:
                session_time = session.time
                session_name = session.name
                session_id = session.session_id
                if session_time not in session_map:
                    session_map[session_time] = []
                session_map[session_time].append((session_name, session_id))
            day_week_map[day_str] = session_map
        week_map[week_key] = day_week_map

    repo = Repository(week_map)

    class_id = repo.find_class_by_id(week_start="21-09-2020", day="27-09-2020",
                                     activity_type="FREE_TRAINING", session_type="Vrij trainen",
                                     start_time="20:30 - 21:30")
    print(f"class_id = {class_id}")

    # subscriber = Subscriber(driver)
    # subscriber.subscribe(class_id)
