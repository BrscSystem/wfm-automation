import os

from winotify import Notification

from config import STATIC_PATH


def notify(title, message):
    icon_path = os.path.abspath(os.path.join(STATIC_PATH, "img", "logo.png"))

    notification = Notification(
        app_id="WFM Automation",
        title=title,
        msg=message,
        icon=icon_path,
        duration="short",
    )

    notification.show()
