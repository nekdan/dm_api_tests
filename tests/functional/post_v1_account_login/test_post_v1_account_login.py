from json import loads

from requests import Response

from dm_api_account.apis.account_api import AccountAPI
from dm_api_account.apis.login_api import LoginAPI
from api_mailhog.apis.mailhog_api import MailhogAPI


def test_post_v1_account_login():
    # Регистрация пользователя
    account_api = AccountAPI(host='http://5.63.153.31:5051')
    login_api = LoginAPI(host='http://5.63.153.31:5051')
    mailhog_api = MailhogAPI(host='http://5.63.153.31:5025')
    login = 'n.danilushkin10'
    email = f'{login}@mail.ru'
    password = '123456'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"Пользователь не был создан {response.json()}"

    # Получить письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "Письма не были получены"

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"


def get_activation_token_by_login(login: str, response: Response) -> str:
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token
