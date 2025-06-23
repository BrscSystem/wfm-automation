from app.automation import automation
from app.screens.login_interface import LoginInterface


def on_clicked_run():
    automation.run_automation(5)


def run():
    LoginInterface()
    on_clicked_run()
