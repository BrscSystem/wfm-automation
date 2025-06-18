import json
import os

from requests import Response, Session
from requests.adapters import HTTPAdapter, Retry
from requests.auth import HTTPBasicAuth

from config import BASEDIR as ROOT_PATH


class Api:
    API_URL = (
        "/adc-intg/api/rest/v1/iTeam/iTeam/iteam_operation_plan_automation"
    )

    def __init__(self):
        self._secret_key = "k.+1wJ-~g0xT5W2,-Xv_$I8sXxfY]8SMG=w*g%y$"
        self._user_id = "101r|MvkV6NqKrummLcwtwVmq"
        self._port = "https://101r-mx.teleows.com"

        self._is_dev_env()

        self._retries = Retry(
            total=5, backoff_factor=2, status_forcelist=[404, 500, 501]
        )

        self._session = Session()
        self._session.mount("https://", HTTPAdapter(max_retries=self._retries))

    def _is_dev_env(self):
        if os.path.exists(os.path.join(ROOT_PATH, "requirements.txt")):
            self._secret_key = "F4+4H(Du(0`r1ELC*4~pC+FMb}xQ^4o-B1vt@FWL"
            self._user_id = "1040|NWMIbnj8hPwqwW0mu3Kf"
            self._port = "https://1040-sg-studio.teleows.com"

    def _get_auth_header(self):
        basic_auth = HTTPBasicAuth(
            username=self._user_id, password=self._secret_key
        )

        return basic_auth

    @staticmethod
    def get_headers():
        return {"Content-Type": "application/json"}

    def upsert(self, payload: dict) -> Response:
        response = self._session.put(
            f"{self._port}{Api.API_URL}/upsert_wfms",
            json=payload,
            headers=self.get_headers(),
            auth=self._get_auth_header(),
            verify=False,
        )

        print(f'\n{len(json.loads(payload["_values"]))} dados enviados\n')

        print(
            f'{len(json.loads(response.content)["results"])} dados recebidos pela API\n'
        )

        return response
