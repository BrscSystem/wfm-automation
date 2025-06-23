from app.data_manager import data_manager as data
from app.pickle_manager import PickleManager


class LoginInterface:
    def __init__(self):
        self.bwx = "bwx1233842"
        self.password = "Slug161120@"

        self.handle_submit()

    def handle_submit(self):
        PickleManager.set_pickle({"user": self.bwx, "password": self.password})
        data.set_username(self.bwx)
        data.set_password(self.password)
