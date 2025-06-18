import os
import sys

BASEDIR = os.path.dirname(os.path.abspath("main.py"))

APPDATA = os.path.join(os.getenv("LOCALAPPDATA"), "iTeam WFM Automation")

PICKLE_FOLDER = os.path.join(APPDATA, "pickle")

WEB_DRIVER_CACHE_FOLDER = os.path.join(APPDATA, "WebDriverCache")

STATIC_PATH = (
    os.path.join(sys._MEIPASS, "static")
    if getattr(sys, "frozen", False)
    else os.path.join(BASEDIR, "app", "static")
)

LOGO_PATH = os.path.join(STATIC_PATH, "img", "logo.png")

ICO_PATH = os.path.join(STATIC_PATH, "img", "logo.ico")

# Check if appdata folder exists
if not os.path.exists(APPDATA):
    os.mkdir(APPDATA)

# Check if pickle folder exists
if not os.path.exists(PICKLE_FOLDER):
    os.mkdir(PICKLE_FOLDER)

# Check if WebDriverCache folder exists
if not os.path.exists(WEB_DRIVER_CACHE_FOLDER):
    os.mkdir(WEB_DRIVER_CACHE_FOLDER)
