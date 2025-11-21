def test_put_v1_account_token(account_helper, prepare_user, auth_account_helper):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    new_password = password + '_new'

    account_helper.register_new_user(login, password, email)
    auth_session = auth_account_helper(login, password)
    auth_session.change_password(login=login, email=email, old_password=password, new_password=new_password)
    auth_session.user_login(login, new_password)

