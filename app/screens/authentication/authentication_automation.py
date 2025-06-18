import time

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from app.data_manager import data_manager as data


class AuthenticationAutomation:
    CHOICE_EMAIL_CODE = '//*[@id="app"]/div[2]/div[3]/div[2]/div/div/div/div[4]/div/div[2]/div[1]'
    GET_CODE = '//*[@id="app"]/div[2]/div[3]/div[2]/div/div/div/div[4]/div/div[1]/div/span/span/span'

    CODE_INPUT = '//*[@id="app"]/div[2]/div[3]/div[2]/div/div/div/div[4]/div/div[1]/div/input'

    ERROR_DIV = (
        '//*[@id="app"]/div[2]/div[3]/div[2]/div/div/div/div[4]/div/div[2]'
    )

    SUBMIT_BUTTON = '//*[@id="app"]/div[2]/div[3]/div[2]/div/div/div/div[4]/div/div[4]/button[2]'

    NETCARE_PAGE = '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]'

    def __init__(self):
        self.browser = data.browser

    def send_code(self, choice):
        if choice == "email":
            self.browser.find_element(By.XPATH, self.CHOICE_EMAIL_CODE).click()
            time.sleep(1)

        # Get Code
        self.browser.find_element(By.XPATH, self.GET_CODE).click()

        return

    def check_code(self, code):
        self.browser.find_element(By.XPATH, self.CODE_INPUT).clear()

        self.browser.find_element(By.XPATH, self.CODE_INPUT).send_keys(code)

        time.sleep(1)

        # Submit
        self.browser.find_element(By.XPATH, self.SUBMIT_BUTTON).click()

        time.sleep(3)

        try:
            if self.browser.find_element(By.XPATH, self.ERROR_DIV):
                return True

            else:
                return False

        except Exception:
            return False
