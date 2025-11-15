import time
from json import loads

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
                    raise AssertionError(f"Превышено количество попыток получения активационного токена [{number_retries}]")
                if token:
                    return token
                time.sleep(delay_seconds)
        return wrapper
    return decorator


class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog: ApiMailhog):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_new_user(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Пользователь не был создан {response.json()}"
        response = self.confirm_by_email(login)
        return response

    def confirm_by_email(self, login: str):
        token = self.get_activation_token_by_login(login)
        assert token is not None, f"Токен для пользователя {login} не был получен"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован"
        return response

    def user_login(self, login: str, password: str, remember_me: bool = True, expected_status_code: int = 200):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == expected_status_code, \
            f"Ошибка авторизации. Ожидался статус-код {expected_status_code}, но получен {response.status_code}"
        return response

    @retrier()
    def get_activation_token_by_login(self, login: str) -> str:
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"
        token = None
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token

    def change_email(self, login: str, password: str, new_email: str):
        json_data = {
            'login': login,
            'password': password,
            'email': new_email,
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, f"Ошибка {response.status_code} - email не изменён"
