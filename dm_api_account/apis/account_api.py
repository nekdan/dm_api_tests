from requests import Response

from restclient.client import RestClient


class AccountAPI(RestClient):
    def post_v1_account(self, json_data: dict[str, str]) -> Response:
        """
        Register new user
        :param json_data: A JSON serializable Python object to send in the body of the :class:`Request`
        :return: The :class:`Response <Response>` object, which contains a server's response to an HTTP request
        """
        response = self.post('/v1/account', json=json_data)
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
        response = self.put(f'/v1/account/{token}', headers=headers)
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
        response = self.put('/v1/account/email', headers=headers, json=json_data)
        return response
