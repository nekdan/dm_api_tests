def test_delete_v1_account_login_all(prepare_user, auth_account_helper, account_helper) -> None:
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    account_helper.register_new_user(login, password, email)
    auth_session = auth_account_helper(login, password)
    auth_session.user_logout_all()
