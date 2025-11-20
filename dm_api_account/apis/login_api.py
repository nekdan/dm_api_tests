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

    def delete_v1_account_login(self, **kwargs) -> Response:
        """
        Logout as current user
        :param kwargs: Keyword arguments
        :return: The :class:`Response <Response>` object, which contains a server's response to an HTTP request
        """
        response = self.delete('/v1/account/login', **kwargs)
        return response

    def delete_v1_account_login_all(self, **kwargs) -> Response:
        """
        Logout from every device
        :param kwargs: Keyword arguments
        :return: The :class:`Response <Response>` object, which contains a server's response to an HTTP request
        """
        response = self.delete('/v1/account/login/all', **kwargs)
        return response
