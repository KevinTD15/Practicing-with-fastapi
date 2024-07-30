auth_prefix = "/login"


def test_user_login(fake_session, fake_user_service, test_client):
    login_data = {"email": "jose@gmail.com", "password": "1234"}
    response = test_client.post(url=auth_prefix, json=login_data)
    assert fake_user_service.user_exists_called_once()
