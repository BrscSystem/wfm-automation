import time

import schedule

from app.automated_pages.login import Login
from app.automated_pages.netcare_page import NetCarePage
from app.data_manager import data_manager
from app.handling_and_sending_data.excel_manipulator import ExcelManipulator
from app.handling_and_sending_data.send_tasks_to_iteam import SendTasksToIteam
from app.notifications import notify
from app.screens.login_interface import LoginInterface


class Automation:
    @staticmethod
    def run_automation(maximum_attempts):
        notify(
            "Your automation is running!",
            "Wait a moment for the process to complete",
        )
        time.sleep(3)

        try:
            data_manager.start_browser()
        except ConnectionError:
            if maximum_attempts > 0:
                time.sleep(2)
                print(
                    f"-------- Connection attempt {maximum_attempts} --------"
                )
                Automation.run_automation(maximum_attempts - 1)
            else:
                notify(
                    "Connection error!",
                    "Run the automation again",
                )

        Automation.start_automation()

    @staticmethod
    def start_automation():
        try:
            login = Login()
            netcare_page = NetCarePage()
            excel_manipulator = ExcelManipulator()

            # Login
            login.start()

            # NetCare Page
            if netcare_page.verify_page():
                netcare_page.configure_columns()

                netcare_page.set_filters()

                netcare_page.export_wfms()

                excel_manipulator.process_tasks()

                SendTasksToIteam(excel_manipulator.json_result)

        except Exception:
            notify(
                "Error when running automation!",
                "Wait a moment and try again",
            )

    @staticmethod
    def change_login():
        LoginInterface()

    @staticmethod
    def start_scheduler():
        schedule.every(5).minutes.do(lambda: automation.run_automation(5))

        while True:
            schedule.run_pending()
            time.sleep(1)


automation = Automation()
