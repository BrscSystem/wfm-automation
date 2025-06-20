import os
import sys
import platform

BASEDIR = os.path.dirname(os.path.abspath("main.py"))

if platform.system() == "Windows":
    LOCAL_APPDATA = os.getenv("LOCALAPPDATA")
    APPDATA = os.path.join(LOCAL_APPDATA, "iTeam WFM Automation")
else:
    # Diretório oculto no home do usuário em Linux/macOS
    APPDATA = os.path.join(os.path.expanduser("~"), ".iteam_wfm_automation")

PICKLE_FOLDER = os.path.join(APPDATA, "pickle")
WEB_DRIVER_CACHE_FOLDER = os.path.join(APPDATA, "WebDriverCache")

STATIC_PATH = (
    os.path.join(sys._MEIPASS, "static")
    if getattr(sys, "frozen", False)
    else os.path.join(BASEDIR, "app", "static")
)

LOGO_PATH = os.path.join(STATIC_PATH, "img", "logo.png")
ICO_PATH = os.path.join(STATIC_PATH, "img", "logo.ico")

# Criação segura de diretórios
os.makedirs(PICKLE_FOLDER, exist_ok=True)
os.makedirs(WEB_DRIVER_CACHE_FOLDER, exist_ok=True)
