def test_post_v1_account_login(prepare_user, account_helper):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    account_helper.register_new_user(login, password, email)
    account_helper.user_login(login, password)
