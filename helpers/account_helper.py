import time
from json import loads

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from services.api_mailhog import ApiMailhog
from services.dm_api_account import DMApiAccount


def retrier(number_retries: int = 3, delay_seconds: int = 1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            token = None
            count = 0
            while token is None:
                print(f"Попытка получения токена №{count}")
                token = func(*args, **kwargs)
                count += 1
                if count > number_retries:
                    raise AssertionError(f"Превышено количество попыток({number_retries}) получения токена")
                if token:
                    return token
                time.sleep(delay_seconds)
        return wrapper
    return decorator


class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog: ApiMailhog):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(self, login: str, password: str):
        response = self.user_login(login=login, password=password)
        token = {
            'x-dm-auth-token': response.headers['x-dm-auth-token']
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def register_new_user(self, login: str, password: str, email: str):
        registration = Registration(
            login=login,
            email=email,
            password=password,
        )
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f"Пользователь не был создан {response.json()}"
        response = self.confirm_by_email(login)
        return response

    def confirm_by_email(self, login: str):
        start_time = time.time()
        token = self.get_activation_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, "Время ожидания активации превышено"
        assert token is not None, f"Токен для пользователя {login} не был получен"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response

    def user_login(self,
                   login: str,
                   password: str,
                   remember_me: bool = True,
                   validate_response: bool = False,
                   validate_heders: bool = False,
                   expected_status_code: int = 200,
                   ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response
        )
        if validate_heders:
            assert response.headers['x-dm-auth-token'], "Токен для пользователя не был получен"
            assert response.status_code == expected_status_code, \
                f"Ошибка авторизации. Ожидался статус-код {expected_status_code}, но получен {response.status_code}"
        return response

    def user_logout(self):
        response = self.dm_account_api.login_api.delete_v1_account_login()
        return response

    def user_logout_all(self):
        response = self.dm_account_api.login_api.delete_v1_account_login_all()
        return response

    def _find_token(self, login: str, key: str) -> str:
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"
        token = None
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login and key in user_data:
                token = user_data[key].split('/')[-1]
        return token

    @retrier()
    def get_activation_token_by_login(self, login: str) -> str:
        return self._find_token(login, 'ConfirmationLinkUrl')

    @retrier()
    def get_reset_token_by_login(self, login: str) -> str:
        return self._find_token(login, 'ConfirmationLinkUri')

    def change_email(self, login: str, password: str, new_email: str):
        change_email = ChangeEmail(
            login=login,
            password=password,
            email=new_email
        )
        self.dm_account_api.account_api.put_v1_account_email(change_email=change_email)

    def reset_password(self, login: str, email: str):
        reset_password = ResetPassword(
            login=login,
            email=email
        )
        self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)

    def change_password(self, login: str, email:str, old_password: str, new_password: str):
        self.reset_password(login, email)
        token = self.get_reset_token_by_login(login=login)
        change_password = ChangePassword(
            login=login,
            token=token,
            oldPassword=old_password,
            newPassword=new_password
        )
        self.dm_account_api.account_api.put_v1_account_password(change_password=change_password)

    def get_user(self, validate_response: bool = True):
        response = self.dm_account_api.account_api.get_v1_account(validate_response)
        return response
