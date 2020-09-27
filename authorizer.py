class Authorizer:
    def __init__(self, driver, base_api):
        self.base_api = base_api
        self.driver = driver

    def authorize(self, now, gym_url, activity_type, email, password):
        driver = self.driver
        driver.get(self.base_api.format(gym_url, now, activity_type))

        login_elem = driver.find_element_by_class_name("btn-login")
        login_elem.click()

        username_elem = driver.find_element_by_id("username")
        password_elem = driver.find_element_by_id("password")
        login_btn = driver.find_element_by_id("login_btn")

        username_elem.send_keys(email)
        password_elem.send_keys(password)
        login_btn.click()

        return driver
