import structlog

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailhogConfiguration
from services.api_mailhog import ApiMailhog
from services.dm_api_account import DMApiAccount

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True),
    ]
)


def test_put_v1_account_email():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = ApiMailhog(configuration=mailhog_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = 'n.danilushkin33'
    email = f'{login}@mail.ru'
    new_login = login + '_new'
    new_email = f'{new_login}@mail.ru'
    password = '123456'

    account_helper.register_new_user(login, email, password)
    account_helper.user_login(login, password)
    account_helper.change_email(login, password, new_email)
    account_helper.user_login(login, password, expected_status_code=403)
    account_helper.confirm_by_email(login)
    account_helper.user_login(login, password)
