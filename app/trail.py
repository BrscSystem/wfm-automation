import pystray
from PIL import Image
from pystray import MenuItem as item

from app.automation import automation
from app.notifications import notify
from app.screens.login_interface import LoginInterface
from config import LOGO_PATH


def on_clicked_run():
    automation.run_automation(5)


def on_clicked_logout():
    notify("Logout requested!", "Enter the new login")
    LoginInterface()


def create_icon():
    icon_path = LOGO_PATH
    return Image.open(icon_path)


def run():
    icon = pystray.Icon("WFM - iTeam")

    icon.icon = create_icon()

    icon.menu = pystray.Menu(
        item("Run", on_clicked_run), item("Logout", on_clicked_logout)
    )

    icon.run()
