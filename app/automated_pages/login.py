import sys
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from app.data_manager import data_manager as data
from app.notifications import notify
from app.screens.login_interface import LoginInterface


class Login:
    UNIPORTAL_BUTTON = '//*[@id="quick-link"]/a[1]'

    FORM_CONTAINER = '//*[@id="container"]/div'
    INPUT_USER = '//*[@id="username"]'
    INPUT_PASSWORD = '//*[@id="password-item"]/div/div[1]/input'
    SUBMIT_BUTTON = '//*[@id="login-btn"]'

    ERROR_LOGIN = '//*[@id="password-item"]/div/div[2]'

    ERROR_AUTHENTICATION = '//*[@id="captcha"]/div[2]/div[2]/div/div'

    def __init__(self):
        self.browser = data.browser

        self.user = data.get_username()
        self.password = data.get_password()

        self.login_credentials()

    def start(self):
        WebDriverWait(self.browser, 60).until(
            EC.any_of(
                EC.presence_of_element_located(
                    (By.XPATH, self.UNIPORTAL_BUTTON)
                ),
                EC.presence_of_element_located((By.XPATH, self.FORM_CONTAINER)),
            )
        )

        if self.browser.find_elements(By.XPATH, self.UNIPORTAL_BUTTON):
            time.sleep(1)
            self.browser.find_element(By.XPATH, self.UNIPORTAL_BUTTON).click()

            WebDriverWait(self.browser, 30).until(
                EC.presence_of_element_located((By.XPATH, self.FORM_CONTAINER))
            )

        self.login_form()

    def login_form(self):
        self.browser.find_element(By.XPATH, self.INPUT_USER).clear()
        self.browser.find_element(By.XPATH, self.INPUT_USER).send_keys(
            data.get_username()
        )

        self.browser.find_element(By.XPATH, self.INPUT_PASSWORD).clear()
        self.browser.find_element(By.XPATH, self.INPUT_PASSWORD).send_keys(
            data.get_password()
        )

        time.sleep(1)

        self.browser.find_element(By.XPATH, self.SUBMIT_BUTTON).click()

        if self.find_error(self.ERROR_LOGIN):
            notify("BWX or Wrong Password!", "Add your login again!")
            LoginInterface()
            self.login_form()
            return

        if self.find_error(self.ERROR_AUTHENTICATION):
            notify(
                "Error!",
                "Unable to proceed with automation, CAPTCHA was called!",
            )

        print("-------- Login - OK --------")

    def login_credentials(self, login_incorrect=False):
        if login_incorrect or not (self.user and self.password):
            LoginInterface()

    def find_error(self, xpath):
        time.sleep(2)
        try:
            if self.browser.find_element(By.XPATH, xpath).is_displayed():
                return True

            else:
                return False

        except Exception:
            return False
