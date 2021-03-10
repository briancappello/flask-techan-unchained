import pytest

from flask_unchained.bundles.security import SecurityService, UserManager, current_user


@pytest.mark.usefixtures('user')
class TestLogin:
    def test_json_login_errors(self, api_client):
        r = api_client.post('security_controller.login',
                            data=dict(email=None, password=None))
        assert 'error' in r.json

    def test_json_login_with_email(self, api_client, user):
        r = api_client.post('security_controller.login',
                            data=dict(email=user.email, password='password'))
        assert r.status_code == 200
        assert 'user' in r.json
        assert 'token' in r.json
        assert r.json['user']['id'] == user.id
        assert current_user == user

    # FIXME
    # def test_json_login_with_username(self, api_client, user):
    #     r = api_client.post('security_controller.login',
    #                         data=dict(email=user.username, password='password'))
    #     assert r.status_code == 200
    #     assert 'user' in r.json
    #     assert 'token' in r.json
    #     assert r.json['user']['id'] == user.id
    #     assert current_user == user

    def test_active_user_required(self, api_client, user, user_manager):
        user.is_active = False
        user_manager.save(user, commit=True)
        r = api_client.post('security_controller.login',
                            data=dict(email=user.email, password='password'))
        assert r.status_code == 401

    @pytest.mark.options(SECURITY_CONFIRMABLE=True)
    def test_confirmed_user_required(self, api_client,
                                     user_manager: UserManager,
                                     security_service: SecurityService):
        user = user_manager.create(username='test',
                                   email='test@example.com',
                                   password='password',
                                   first_name='the',
                                   last_name='user',
                                   is_active=True)
        security_service.register_user(user)

        r = api_client.post('security_controller.login',
                            data=dict(email=user.email, password='password'))
        assert r.status_code == 401
        assert 'Email requires confirmation.' == r.json['error']
