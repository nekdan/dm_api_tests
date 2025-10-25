import requests
from requests import Response


class LoginAPI:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def post_v1_account_login(self, json_data: dict[str, str | bool]) -> Response:
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = requests.post(f'{self.host}/v1/account/login', json=json_data)
        return response
