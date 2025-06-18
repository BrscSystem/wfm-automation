from customtkinter import CTk, CTkButton, CTkEntry, CTkLabel

from app.data_manager import data_manager as data
from app.pickle_manager import PickleManager
from app.screens.base_interface import BaseInterface
from config import ICO_PATH


class LoginInterface(BaseInterface):
    def __init__(self, title="iTeam WFM Automation", width=400, height=220):
        self.interface = CTk()

        self.bwx = None
        self.password = None

        self.user_login_label = None
        self.login_entry = None
        self.user_password_label = None
        self.password_entry = None
        self.submit_button = None

        self.interface_configuration(title, width, height)

        self.create_components()

        self.display_components()

        self.interface.mainloop()

    def create_components(self):
        self.user_login_label = CTkLabel(
            self.interface, text="Username", text_color="#A1A5A1"
        )
        self.login_entry = CTkEntry(
            master=self.interface, width=300, height=34, text_color="#EAEAEA"
        )
        self.user_password_label = CTkLabel(
            self.interface, text="Password", text_color="#A1A5A1"
        )
        self.password_entry = CTkEntry(
            master=self.interface,
            width=300,
            height=34,
            text_color="#EAEAEA",
            show="*",
        )
        self.submit_button = CTkButton(
            master=self.interface,
            text="Submit",
            command=self.handle_submit,
            width=300,
            height=34,
            fg_color="#017c29",
            hover_color="#329e29",
        )

    def display_components(self):
        self.user_login_label.place(relx=0.13, rely=0.12, anchor="w")
        self.login_entry.place(relx=0.5, rely=0.25, anchor="center")
        self.user_password_label.place(relx=0.13, rely=0.4, anchor="w")
        self.password_entry.place(relx=0.5, rely=0.53, anchor="center")
        self.submit_button.place(relx=0.5, rely=0.8, anchor="center")

    def handle_submit(self):
        self.bwx = self.login_entry.get()
        self.password = self.password_entry.get()

        PickleManager.set_pickle({"user": self.bwx, "password": self.password})
        data.set_username(self.bwx)
        data.set_password(self.password)

        self.interface.destroy()

    def interface_configuration(self, title, width, height):
        self.interface.title(title)
        self.interface.iconbitmap(ICO_PATH)
        self.interface.geometry(f"{width}x{height}")
        self.interface.resizable(False, False)
