from requests import Response

from restclient.client import RestClient


class LoginAPI(RestClient):
    def post_v1_account_login(self, json_data: dict[str, str | bool]) -> Response:
        """
        Authenticate via credentials
        :param json_data: A JSON serializable Python object to send in the body of the :class:`Request`
        :return: The :class:`Response <Response>` object, which contains a server's response to an HTTP request
        """
        response = self.post('/v1/account/login', json=json_data)
        return response
