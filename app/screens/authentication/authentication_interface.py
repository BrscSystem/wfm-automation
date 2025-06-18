import threading
import time

from customtkinter import (
    CTk,
    CTkButton,
    CTkEntry,
    CTkFrame,
    CTkLabel,
    CTkProgressBar,
)

from app.screens.authentication.authentication_automation import (
    AuthenticationAutomation,
)
from app.screens.base_interface import BaseInterface
from config import ICO_PATH


class AuthenticationInterface(BaseInterface):
    def __init__(self, title="iTeam WFM Automation", width=400, height=220):
        self.interface = CTk()
        self.start_time = None
        self.choice = None
        self.code = None

        self.initial_frame = None
        self.label = None
        self.sms_button = None
        self.email_button = None

        self.input_frame = None
        self.input_label = None
        self.input_entry = None
        self.back_button = None
        self.submit_button = None

        self.error_frame = None
        self.error_label = None
        self.try_again_button = None
        self.get_new_code_button = None

        self.loading_back_button = None
        self.loading_back_label = None

        self.loading_frame = None
        self.loading_label = None
        self.loading_spinner = None

        self.automation = AuthenticationAutomation()

        self.interface_configuration(title, width, height)
        self.create_components()
        self.display_components()
        self.interface.mainloop()

    def create_components(self):
        self.initial_frame = CTkFrame(self.interface)
        self.label = CTkLabel(
            self.initial_frame, text="Choose your authentication:"
        )
        self.sms_button = CTkButton(
            self.initial_frame,
            text="SMS",
            command=lambda: self.start_loading("sms"),
        )
        self.email_button = CTkButton(
            self.initial_frame,
            text="EMAIL",
            command=lambda: self.start_loading("email"),
        )

        self.input_frame = CTkFrame(self.interface)
        self.input_label = CTkLabel(
            self.input_frame, text="Enter your authentication code:"
        )
        self.input_entry = CTkEntry(self.input_frame, width=296, height=34)
        self.back_button = CTkButton(
            self.input_frame,
            text="Back",
            command=self.show_initial_frame,
            text_color="#323630",
            fg_color="#B8BDB5",
            hover_color="#D6D9D4",
        )
        self.submit_button = CTkButton(
            self.input_frame,
            text="Submit",
            command=self.handle_submit,
            fg_color="#017c29",
            hover_color="#329E29",
        )

        self.error_frame = CTkFrame(self.interface)
        self.error_label = CTkLabel(self.error_frame, text="Código Incorreto!")
        self.try_again_button = CTkButton(
            self.error_frame,
            text="Try Again",
            command=lambda: self.show_input_frame(self.choice, True),
            text_color="#323630",
            fg_color="#B8BDB5",
            hover_color="#D6D9D4",
        )
        self.get_new_code_button = CTkButton(
            self.error_frame,
            text="Get New Code",
            command=lambda: self.show_initial_frame(True),
            fg_color="#017c29",
            hover_color="#329E29",
        )

        self.loading_back_button = CTkFrame(self.interface)
        self.loading_back_label = CTkLabel(
            self.loading_back_button,
            text="Aguarde alguns segundos para poder pedir um novo código...",
        )

        self.loading_frame = CTkFrame(self.interface)
        self.loading_label = CTkLabel(self.loading_frame, text="Loading...")
        self.loading_spinner = CTkProgressBar(
            self.loading_frame, mode="indeterminate"
        )

    def display_components(self):
        self.initial_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.label.place(relx=0.5, rely=0.3, anchor="center")
        self.sms_button.place(relx=0.3, rely=0.55, anchor="center")
        self.email_button.place(relx=0.7, rely=0.55, anchor="center")

        self.input_label.place(relx=0.5, rely=0.22, anchor="center")
        self.input_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.back_button.place(relx=0.3, rely=0.67, anchor="center")
        self.submit_button.place(relx=0.7, rely=0.67, anchor="center")

        self.error_label.place(relx=0.5, rely=0.3, anchor="center")
        self.get_new_code_button.place(relx=0.7, rely=0.55, anchor="center")
        self.try_again_button.place(relx=0.3, rely=0.55, anchor="center")

        self.loading_back_label.place(relx=0.5, rely=0.45, anchor="center")

        self.loading_label.place(relx=0.5, rely=0.3, anchor="center")
        self.loading_spinner.place(relx=0.5, rely=0.4, anchor="center")

    def handle_submit(self):
        self.code = self.input_entry.get()
        if not self.automation.check_code(self.code):
            self.interface.destroy()
            return
        else:
            self.show_error_frame()

    def interface_configuration(self, title, width, height):
        self.interface.title(title)
        self.interface.iconbitmap(ICO_PATH)
        self.interface.geometry(f"{width}x{height}")
        self.interface.resizable(False, False)

    def show_input_frame(self, auth, try_again=False):
        self.initial_frame.place_forget()
        self.choice = auth

        if try_again:
            self.error_frame.place_forget()

        else:
            if self.start_time is not None:
                self.loading_back_button.place(
                    relx=0, rely=0, relwidth=1, relheight=1
                )
                while (time.time() - self.start_time) < 60:
                    time.sleep(1)

                self.input_entry.delete(0, "end")
                self.loading_back_button.place_forget()

            self.automation.send_code(self.choice)
            self.start_time = time.time()

        self.input_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_initial_frame(self, get_new_code=False):
        self.input_frame.place_forget()

        if get_new_code:
            self.error_frame.place_forget()

        self.initial_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_error_frame(self):
        self.input_frame.place_forget()
        self.error_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def start_loading(self, auth):
        self.choice = auth
        self.initial_frame.place_forget()
        self.loading_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.loading_spinner.start()

        threading.Thread(target=self.loading, args=(auth,), daemon=True).start()

    def loading(self, auth):
        time.sleep(2)
        self.loading_spinner.stop()
        self.loading_frame.place_forget()
        self.show_input_frame(auth)
