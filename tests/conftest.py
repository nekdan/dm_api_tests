from collections import namedtuple
from datetime import datetime

import pytest
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


@pytest.fixture(scope='session')
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025', disable_log=True)
    mailhog_client = ApiMailhog(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope='session')
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=True)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture(scope='session')
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture(scope='session')
def auth_account_helper(mailhog_api):
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    def _auth(login, password):
        account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
        account_helper.auth_client(login=login, password=password)
        return account_helper
    return _auth


@pytest.fixture
def prepare_user():
    now = datetime.now()
    data = now.strftime('%d_%m_%Y_%H_%M_%S')
    login = f'n.danilushkin_{data}'
    password = '123456'
    email = f'{login}@mail.ru'
    User = namedtuple('user', ['login', 'password', 'email'])
    user = User(login=login, password=password, email=email)
    return user
