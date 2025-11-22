from hamcrest import assert_that, all_of, has_property, has_properties, equal_to, \
    contains_inanyorder

from dm_api_account.models.user_details_envelope import UserRole


def test_get_v1_account_auth(auth_account_helper) -> None:
    login = 'n.danilushkin'
    auth_session = auth_account_helper(login=login, password='123456')
    response = auth_session.get_user()
    print("Test:", response)
    assert_that(
        response, all_of(
            has_property('resource', has_property('login', equal_to(login))),
            has_property(
                'resource', has_properties(
                    {
                        "rating": has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                    }
                )
            ),
            has_property('resource', has_property('roles', contains_inanyorder(UserRole.GUEST, UserRole.PLAYER)))
        )
    )

def test_get_v1_account_no_auth(account_helper) -> None:
    account_helper.get_user(validate_response=False)
