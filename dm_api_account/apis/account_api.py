import requests
from requests import Response


class AccountAPI:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def post_v1_account(self, json_data: dict[str, str]) -> Response:
        """
        Register new user
        :param json_data:
        :return:
        """
        response = requests.post(f'{self.host}/v1/account', json=json_data)
        return response

    def put_v1_account_token(self, token) -> Response:
        """
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }
        response = requests.put(f'{self.host}/v1/account/{token}', headers=headers)
        return response