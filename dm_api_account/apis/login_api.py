from requests import Response

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class LoginAPI(RestClient):
    def post_v1_account_login(self,
                              login_credentials: LoginCredentials,
                              validate_response: bool = True
                              ) -> UserEnvelope | Response:
        """
        Authenticate via credentials
        :param login_credentials: A JSON serializable Python object to send in the body of the :class:`Request`
        :param validate_response: Flag indicating whether to validate the response and return a UserEnvelope object
        :return: The :class:`Response <Response>` object, which contains a server's response to an HTTP request
        """
        response = self.post('/v1/account/login', json=login_credentials.model_dump(exclude_none=True, by_alias=True))
        return UserEnvelope(**response.json()) if validate_response else response

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
