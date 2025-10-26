import requests
from requests import Response


class AccountAPI:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def post_v1_account(self, json_data: dict[str, str]) -> Response:
        """
        Register new user
        :param json_data: A JSON serializable Python object to send in the body of the :class:`Request`
        :return: The :class:`Response <Response>` object, which contains a server's response to an HTTP request
        """
        response = requests.post(f'{self.host}/v1/account', json=json_data)
        return response

    def put_v1_account_token(self, token: str) -> Response:
        """
        Activate registered user
        :param token: User token in UUID format
        :return: The :class:`Response <Response>` object, which contains a server's response to an HTTP request
        """
        headers = {
            'accept': 'text/plain',
        }
        response = requests.put(f'{self.host}/v1/account/{token}', headers=headers)
        return response

    def put_v1_account_email(self, json_data: dict[str, str]) -> Response:
        """
        Change registered user email
        :param json_data: A JSON serializable Python object to send in the body of the :class:`Request`
        :return: The :class:`Response <Response>` object, which contains a server's response to an HTTP request
        """
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }
        response = requests.put(f'{self.host}/v1/account/email', headers=headers, json=json_data)
        return response
