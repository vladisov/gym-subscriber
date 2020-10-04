import time

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class Subscriber:
    def __init__(self, driver):
        self.driver = driver

    def subscribe(self, class_id):
        driver = self.driver
        count = 1
        while True:
            sesh = driver.find_element_by_id(class_id)
            sesh.click()
            time.sleep(1)
            confirmation = driver.find_elements_by_id("pre_booking_confirmation")
            if len(confirmation) > 0:
                confirmation[0].click()
                book = driver.find_element_by_id("book_btn")
                book.click()
                time.sleep(1)
                print("signed up successfully !!!")
                break
            time.sleep(1)
            print('no spots available :( , attempt number - {0}!'.format(count))
            count += 1
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(5)
