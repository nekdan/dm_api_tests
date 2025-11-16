def test_put_v1_account_token(account_helper, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    account_helper.register_new_user(login, password, email)
    account_helper.user_login(login, password)
    account_helper.dm_account_api.account_api.get_v1_account()
