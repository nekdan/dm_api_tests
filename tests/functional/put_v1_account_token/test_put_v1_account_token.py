def test_put_v1_account_token(prepare_user, account_helper):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    account_helper.register_new_user(login, password, email)
