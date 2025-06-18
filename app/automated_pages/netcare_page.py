import time
from datetime import datetime, timedelta

import pytz
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from app.data_manager import data_manager as data
from app.screens.authentication.authentication_interface import (
    AuthenticationInterface,
)


class NetCarePage:
    AUTH_ELEMENT = '//*[@id="app"]/div[2]/div[3]/div[2]/div/div/div/div[4]/div/div[1]/div/span/span/span'
    NETCARE_ELEMENT = '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]'

    # Filters
    CONFIGURATION_FILTER = '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]/form/div[1]/div[10]/button'
    SELECT_ALL_CONFIGURATION = '//label[contains(@class, "el-checkbox") and contains(@class, "checked-all")]'
    PRODUCT_SKILL_DOMAIN_CONFIGURATION = (
        '//div[text()=" Product Skill Domain"]/label'
    )
    OK_BUTTON_CONFIGURATION = "/html/body/div[3]/div/div/footer/div/button[1]"

    ICT_OPERATION_SCENARIO = (
        '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]/form/div[1]/div[1]/div/div/div/div['
        "1]/div[2]"
    )
    TASK_START_TIME = '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]/form/div[1]/div[5]/div/div/div'
    TASK_START_TIME_CLEAR = '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]/form/div[1]/div[5]/div/div/div/span[2]/span'

    EXIT_THE_DATE_COMPONENT = (
        '//*[@id="app"]/div/div/div[2]/div[1]/div[1]/div/div/span[1]'
    )

    TO_CLEAR = '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]/form/div[1]/div[6]/div/div/div/span[2]/span'
    TO = '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]/form/div[1]/div[6]/div/div/div'

    ADVANCED_SEARCH = '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]/form/div[1]/div[9]/button'
    REGION = '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]/form/div[2]/div[1]/div/div/div'
    REP_OFFICE = '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]/form/div[2]/div[2]/div/div/div'
    TASK_TYPE = '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]/form/div[2]/div[9]/div/div/div'
    WAIT_TASK_TYPE = '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]/form/div[2]/div[9]/div/div/div/div[1]/div[1]/span'

    # Search and Export
    SEARCH_BUTTON = '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]/form/div[1]/div[7]/button'
    EXPORT_HOVER = '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]/form/div[1]/div[12]/div'
    ALL_EXPORT_BUTTON = ".//li[text()=' Export all']"

    def __init__(self):
        self.browser = data.browser
        self.midnight_today, self.midnight_tomorrow = NetCarePage.get_dates()

    def verify_page(self):
        try:
            WebDriverWait(self.browser, 60).until(
                EC.any_of(
                    EC.presence_of_element_located(
                        (By.XPATH, self.NETCARE_ELEMENT)
                    ),
                    EC.presence_of_element_located(
                        (By.XPATH, self.AUTH_ELEMENT)
                    ),
                )
            )

            if self.browser.find_elements(By.XPATH, self.NETCARE_ELEMENT):
                return True

            elif self.browser.find_elements(By.XPATH, self.AUTH_ELEMENT):
                return AuthenticationInterface()

        except TimeoutException:
            return False

    def set_filters(self):
        # ICT
        self.find_in_select(self.ICT_OPERATION_SCENARIO, "Carrier")

        # Task Start Time
        self.filling_in_dates(
            self.TASK_START_TIME,
            self.TASK_START_TIME_CLEAR,
            self.midnight_today,
        )

        # TO
        self.filling_in_dates(self.TO, self.TO_CLEAR, self.midnight_tomorrow)

        # Advanced Search
        self.browser.find_element(By.XPATH, self.ADVANCED_SEARCH).click()

        # - Region
        self.find_in_select(self.REGION, "Latin America Region")

        # - Rep Office
        self.find_in_select(self.REP_OFFICE, "Brazil Rep Office")

        # - Task Type
        self.find_in_select(
            self.TASK_TYPE, "Network Operation - Change Implementation"
        )

    def configure_columns(self):
        configuration_element = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, self.CONFIGURATION_FILTER)
            )
        )

        configuration_element.click()

        checkbox = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.SELECT_ALL_CONFIGURATION)
            )
        )

        if "is-checked" not in checkbox.get_attribute("class"):
            checkbox.click()

        time.sleep(2)

        product_skill_domain = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, self.PRODUCT_SKILL_DOMAIN_CONFIGURATION)
            )
        )

        if "is-checked" in product_skill_domain.get_attribute("class"):
            product_skill_domain.click()

        time.sleep(2)

        self.browser.find_element(
            By.XPATH, self.OK_BUTTON_CONFIGURATION
        ).click()

        time.sleep(2)

    def export_wfms(self):
        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, self.WAIT_TASK_TYPE))
        )

        self.browser.find_element(By.XPATH, self.SEARCH_BUTTON).click()
        time.sleep(2)

        export_element = self.browser.find_element(By.XPATH, self.EXPORT_HOVER)
        hover = ActionChains(self.browser).move_to_element(export_element)
        hover.perform()

        time.sleep(1)

        export_item = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, self.ALL_EXPORT_BUTTON))
        )

        time.sleep(1)
        export_item.click()

        print("-------- Exported Data - OK --------")

    def find_in_select(self, dropdown, text):
        element_dropdown = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, dropdown))
        )

        ActionChains(self.browser).move_to_element(
            element_dropdown
        ).click().send_keys(text).perform()
        time.sleep(2)

        actions = ActionChains(self.browser)
        time.sleep(1)
        actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    def filling_in_dates(self, date_input, clear_button, new_date):
        date_element = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, date_input))
        )
        date_element.click()

        to_clear_element = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, clear_button))
        )
        to_clear_element.click()

        ActionChains(self.browser).move_to_element(
            date_element
        ).click().send_keys(new_date).perform()

        time.sleep(1)

        exit_the_date_element = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, self.EXIT_THE_DATE_COMPONENT)
            )
        )
        exit_the_date_element.click()

    @staticmethod
    def get_dates() -> tuple:
        br_tz = pytz.timezone("America/Sao_Paulo")

        now = datetime.now(br_tz)

        midnight_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        midnight_tomorrow = midnight_today + timedelta(days=1)

        formatted_today = midnight_today.strftime("%Y-%m-%d %H:%M:%S")
        formatted_tomorrow = midnight_tomorrow.strftime("%Y-%m-%d %H:%M:%S")

        return formatted_today, formatted_tomorrow
