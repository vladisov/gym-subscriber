from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Driver:

    @staticmethod
    def build():
        options = Options()
        options.headless = True
        return webdriver.Chrome('./chromedriver', options=options)
