from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from repository import Repository


def init_driver():
    options = Options()
    options.headless = True
    return webdriver.Chrome('./chromedriver', options=options)


if __name__ == '__main__':
    # base_api = "https://{0}/classes/week/{1}"
    # "?event_type={2}&coach=0&activity_id=0&member_id_filter=0&embedded=0&planner_type={2}"
    # "&show_personnel_schedule=0&in_app=0&single_club=0"
    # email = sys.argv[1]
    # password = sys.argv[2]
    # gym_url = sys.argv[3]
    # now = datetime.now().strftime("%Y-%m-%d")
    # activity_type = ActivityType.FREE_TRAINING
    #
    # driver = init_driver()
    #
    # authorizer = Authorizer(driver, base_api)
    # driver = authorizer.authorize(now, gym_url, activity_type, email, password)

    # parser = Parser(driver, now, activity_type)
    # weeks = parser.parse(5)

    repo = Repository()
    # repo.insert(weeks)

    class_id = repo.find_class_by_id(week_start="21-09-2020", day="27-09-2020",
                                     activity_type="FREE_TRAINING", session_type="Vrij trainen",
                                     start_time="20:30 - 21:30")
    print(f"class_id = {class_id}")
    # subscriber = Subscriber(driver)
    # subscriber.subscribe(class_id)
