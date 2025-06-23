import time

from app.screens.authentication.authentication_automation import (
    AuthenticationAutomation,
)


class AuthenticationInterface:
    def __init__(self):
        self.automation = AuthenticationAutomation()
        self.auth_method = "sms"
        self.start_authentication()

    def start_authentication(self):
        print(f"Iniciando autenticação via {self.auth_method.upper()}...")
        self.automation.send_code(self.auth_method)
        time.sleep(2)

        code = input("Digite o código recebido: ").strip()

        if self.automation.check_code(code):
            print("✅ Autenticação bem-sucedida.")
        else:
            print("❌ Código incorreto. Abortando.")
            exit(1)
