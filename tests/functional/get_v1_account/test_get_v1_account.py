def test_get_v1_account_auth(auth_account_helper) -> None:
    auth_session = auth_account_helper(login='n.danilushkin', password='123456')
    auth_session.get_user()

def test_get_v1_account_no_auth(account_helper) -> None:
    account_helper.get_user()
