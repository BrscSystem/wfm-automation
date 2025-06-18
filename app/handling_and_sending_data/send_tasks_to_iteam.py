import json
from typing import Any

from app.handling_and_sending_data.api import Api
from app.notifications import notify


class SendTasksToIteam:
    def __init__(self, tasks: list[dict[str, Any]]):
        self.maximum_attempts = 3

        self._api = Api()
        self._tasks = tasks

        self.up_tasks()

    def up_tasks(self) -> dict:
        json_response: dict = {}

        try:
            api_response = self._api.upsert(payload={"_values": self._tasks})

            json_response = json.loads(api_response.content)

            if api_response.status_code == 200:
                notify("Automation ended", "Data successfully sent to iTeam")
                print("-------- Send Data - OK --------")
                return json_response

            else:
                notify("Automation ended", "Data not sent to iTeam")
            return json_response

        except Exception as e:
            print(
                f"Attempt {self.maximum_attempts} to send ows data. \nError: {e}"
            )
            if self.maximum_attempts >= 1:
                self.maximum_attempts -= 1
                return self.up_tasks()

            else:
                notify(
                    "Automation ended",
                    "Invalid network, change it and run again",
                )
                print(f"Error: {e}")
