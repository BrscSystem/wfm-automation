import os
import pickle

from config import PICKLE_FOLDER


class PickleManager:
    @staticmethod
    def get_pickle():
        try:
            with open(os.path.join(PICKLE_FOLDER, "email.pkl"), "rb") as file:
                loaded_data = pickle.load(file)
        except Exception:
            with open(os.path.join(PICKLE_FOLDER, "email.pkl"), "wb") as file:
                data_to_save = {"user": "", "password": ""}
                pickle.dump(data_to_save, file)
                return data_to_save
        return loaded_data

    @staticmethod
    def set_pickle(data):
        saved_data = PickleManager.get_pickle()
        data_to_save = {**saved_data, **data}

        with open(os.path.join(PICKLE_FOLDER, "email.pkl"), "wb") as file:
            pickle.dump(data_to_save, file)
