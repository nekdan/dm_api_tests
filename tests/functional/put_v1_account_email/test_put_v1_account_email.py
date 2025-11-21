def test_put_v1_account_email(prepare_user, account_helper):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    new_login = login + '_new'
    new_email = f'{new_login}@mail.ru'

    account_helper.register_new_user(login, password, email)
    account_helper.user_login(login, password)
    account_helper.change_email(login, password, new_email)
    account_helper.user_login(login, password, expected_status_code=403)
    account_helper.confirm_by_email(login)
    account_helper.user_login(login, password)
