import time
from datetime import datetime

from redis import Redis
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from model.training_model import ActivityType
from task.authorizer import Authorizer
from task.driver import Driver

base_api = "https://{0}/classes/week/{1}"
"?event_type={2}&coach=0&activity_id=0&member_id_filter=0&embedded=0&planner_type={2}"
"&show_personnel_schedule=0&in_app=0&single_club=0"
email = 'YOUR_EMAIL'
password = 'YOUR_PASS'
gym_url = 'GYM_URL'
now = datetime.now().strftime("%Y-%m-%d")
activity_type = ActivityType.FREE_TRAINING


def _init_and_authorize():
    driver = Driver.build()
    authorizer = Authorizer(driver, base_api)
    driver = authorizer.authorize(now, gym_url, activity_type, email, password)
    return driver


class SubscribeTask:

    def __init__(self, job_id, class_id):
        self.class_id = class_id
        self.job_id = job_id
        # self.redis = Redis()

    def __call__(self):
        print('authorizing...')
        driver = _init_and_authorize()
        print('authorized successfully')
        self.subscribe(driver, Redis())

    def subscribe(self, driver, redis):
        print(f"trying to subscribe on {self.class_id}")
        count = 1
        running = True
        while running:
            try:
                status = redis.get(self.job_id).decode("utf-8")
                print(f'job status = {status}')
                if status != 'RUNNING':
                    print(f'thread execution stopped')
                    return

                sesh = driver.find_element_by_id(self.class_id)
                sesh.click()
                time.sleep(1)
                confirmation = driver.find_elements_by_id("pre_booking_confirmation")
                if len(confirmation) > 0:
                    confirmation[0].click()
                    book = driver.find_element_by_id("book_btn")
                    book.click()
                    time.sleep(1)
                    print("signed up successfully !!!")
                    running = False
                    break
                time.sleep(1)
                print('no spots available :( , attempt number - {0}!'.format(count))
                count += 1
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(3)
            except Exception as e:
                print(e)
