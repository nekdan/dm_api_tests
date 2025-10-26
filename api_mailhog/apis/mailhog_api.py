import requests
from requests import Response


class MailhogAPI:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def get_api_v2_messages(self, limit: int = 50) -> Response:
        """
        Get Users emails
        :param limit: The maximum number of emails to return
        :return: The `Response <Response>` object, which contains a server's response to an HTTP request
        """
        params = {
            'limit': limit,
        }
        response = requests.get(f'{self.host}/api/v2/messages', params=params, verify=False)
        return response
