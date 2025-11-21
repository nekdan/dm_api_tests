from requests import Response

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountAPI(RestClient):
    def post_v1_account(self, registration: Registration) -> Response:
        """
        Register new user
        :param registration: Pydantic model
        :return: The :class:`Response <Response>` object, which contains a server's response to an HTTP request
        """
        response = self.post('/v1/account', json=registration.model_dump(exclude_none=True, by_alias=True))
        return response

    def get_v1_account(self, validate_response: bool = True, **kwargs) -> UserDetailsEnvelope | Response:
        """
        Get current user
        :param validate_response: Flag indicating whether to validate the response and return a UserDetailsEnvelope object
        :return: The :class:`Response <Response>` object, which contains a server's response to an HTTP request
        """
        response = self.get('/v1/account', **kwargs)
        return UserDetailsEnvelope(**response.json()) if validate_response else response

    def put_v1_account_token(self, token: str, validate_response: bool = True) -> UserEnvelope | Response:
        """
        Activate registered user
        :param validate_response: Flag indicating whether to validate the response and return a UserEnvelope object
        :param token: User token in UUID format
        :return: The :class:`Response <Response>` object, which contains a server's response to an HTTP request
        """
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(f'/v1/account/{token}', headers=headers)
        return UserEnvelope if validate_response else response

    def put_v1_account_email(self, change_email: ChangeEmail, validate_response: bool = True) -> UserEnvelope | Response:
        """
        Change registered user email
        :param change_email: Pydantic model
        :param validate_response: Flag indicating whether to validate the response and return a UserEnvelope object
        :return: The :class:`Response <Response>` object, which contains a server's response to an HTTP request
        """
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }
        response = self.put('/v1/account/email', headers=headers,
                            json=change_email.model_dump(exclude_none=True, by_alias=True))
        return UserEnvelope(**response.json()) if validate_response else response

    def put_v1_account_password(self,
                                change_password: ChangePassword,
                                validate_response: bool = True
                                ) -> UserEnvelope | Response:
        """
        Change registered user password
        :param change_password: Pydantic model
        :param validate_response: Flag indicating whether to validate the response and return a UserEnvelope object
        :return: The :class:`Response <Response>` object, which contains a server's response to an HTTP request
        """
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }
        response = self.put('/v1/account/password', headers=headers,
                            json=change_password.model_dump(exclude_none=True, by_alias=True, mode='json'))
        return UserEnvelope(**response.json()) if validate_response else response

    def post_v1_account_password(self,
                                 reset_password: ResetPassword,
                                 validate_response: bool = True
                                 ) -> UserEnvelope | Response:
        """
        Change registered user password
        :param reset_password: Pydantic model
        :param validate_response: Flag indicating whether to validate the response and return a UserEnvelope object
        :return: The :class:`Response <Response>` object, which contains a server's response to an HTTP request
        """
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }
        response = self.post('/v1/account/password', headers=headers,
                             json=reset_password.model_dump(exclude_none=True, by_alias=True))
        return UserEnvelope(**response.json()) if validate_response else response
