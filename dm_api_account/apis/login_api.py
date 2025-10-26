import requests
from requests import Response


class LoginAPI:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def post_v1_account_login(self, json_data: dict[str, str | bool]) -> Response:
        """
        Authenticate via credentials
        :param json_data: A JSON serializable Python object to send in the body of the :class:`Request`
        :return: The :class:`Response <Response>` object, which contains a server's response to an HTTP request
        """
        response = requests.post(f'{self.host}/v1/account/login', json=json_data)
        return response
