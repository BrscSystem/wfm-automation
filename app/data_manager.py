import glob
import os
import platform
import time
import uuid

import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from app.notifications import notify
from app.pickle_manager import PickleManager
from config import STATIC_PATH, WEB_DRIVER_CACHE_FOLDER


class DataManager:
    def __init__(self):
        self.browser = None
        self.chrome_driver = None
        self.edge_driver = None
        self.options = Options()
        self.cache_manager = DriverCacheManager(
            root_dir=WEB_DRIVER_CACHE_FOLDER, valid_range=14
        )

        self._username = PickleManager.get_pickle()["user"]
        self._password = PickleManager.get_pickle()["password"]

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def set_username(self, username):
        self._username = username

    def set_password(self, password):
        self._password = password

    def start_browser(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        os.environ["WDM_SSL_VERIFY"] = "0"

        self.options.add_argument("--headless")
        self.find_driver_in_cache()

        system = platform.system()

        if system == "Linux":
            self.start_chrome_browser()
        else:
            try:
                self.start_edge_browser()
            except Exception as e:
                print(f"Edge falhou: {e}")
                self.start_chrome_browser()

        self.access_the_netcare_website()

    def start_chrome_browser(self):

        self.options = webdriver.ChromeOptions()
        self.options.binary_location = os.environ.get("CHROME_BIN", "/usr/bin/chromium")
        self.options.add_argument("--headless=new")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--remote-debugging-port=9222")
        self.options.add_argument("--user-data-dir=/tmp/chrome_user_data")

        self.browser = webdriver.Chrome(
            service=ChromeService("/usr/bin/chromedriver"),
            options=self.options,
        )

        for attempt in range(5):
            try:
                driver_path = ChromeDriverManager(
                    cache_manager=self.cache_manager
                ).install()

                if platform.system() == "Linux":
                    os.chmod(driver_path, 0o755)

                self.browser = webdriver.Chrome(
                    service=ChromeService(driver_path),
                    options=self.options,
                )
                print("-------- Webdriver (Chrome) - OK --------")
                break

            except Exception as e:
                print(
                    f"Attempt {attempt + 1} to launch Chrome browser failed: {e}"
                )
                if attempt == 4:
                    print(
                        "Unable to initialize Chrome after multiple attempts."
                    )
                time.sleep(2)

    def start_edge_browser(self):
        for attempt in range(5):
            try:
                self.browser = webdriver.Edge(
                    service=EdgeService(
                        executable_path=EdgeChromiumDriverManager(
                            cache_manager=self.cache_manager
                        ).install()
                    ),
                    options=self.options,
                )
                print("-------- Webdriver (Edge) - OK --------")
                break

            except Exception as e:
                if self.edge_driver:
                    os.chmod(self.edge_driver, 0o755)
                    self.browser = webdriver.Edge(
                        service=EdgeService(self.edge_driver),
                        options=self.options,
                    )
                    print("-------- Webdriver (Edge) from cache - OK  --------")
                    break

                print(
                    f"Attempt {attempt + 1} to launch Edge browser failed: {e}"
                )
                if attempt == 4:
                    print("Unable to initialize Edge after multiple attempts.")
                time.sleep(2)

    def access_the_netcare_website(self):
        for attempt in range(5):
            try:
                self.browser.get(
                    "https://netcareclient.service.huawei.com/taskmanager/index.html#/TodoTaskList"
                )
                print("-------- Open Netcare Website - OK --------")
                break
            except Exception:
                print(
                    f"Attempt {attempt + 1} to launch the site in browser failed."
                )
                if attempt == 4:
                    notify(
                        "Error!",
                        "Unable to access the page, check your network! URL:https://netcareclient.service.huawei.com/taskmanager/index.html#/TodoTaskList",
                    )
                time.sleep(2)

    def find_driver_in_cache(self):
        edge_driver_files = glob.glob(
            os.path.join(
                f"{WEB_DRIVER_CACHE_FOLDER}/.wdm/drivers",
                "**",
                "msedgedriver",
            ),
            recursive=True,
        )

        chrome_driver_files = glob.glob(
            os.path.join(
                f"{WEB_DRIVER_CACHE_FOLDER}/.wdm/drivers",
                "**",
                "chromedriver",
            ),
            recursive=True,
        )

        if not (edge_driver_files or chrome_driver_files):
            edge_driver_files = glob.glob(
                os.path.join(f"{STATIC_PATH}/drivers", "msedgedriver"),
                recursive=True,
            )

            chrome_driver_files = glob.glob(
                os.path.join(f"{STATIC_PATH}/drivers", "chromedriver"),
                recursive=True,
            )

            print("-------- Local Drivers - OK --------")

        self.edge_driver = edge_driver_files[0] if edge_driver_files else None
        self.chrome_driver = (
            chrome_driver_files[0] if chrome_driver_files else None
        )


data_manager = DataManager()
