import pytest

from flask_unchained.bundles.security import AnonymousUser, current_user


@pytest.mark.usefixtures('user')
class TestLogout:
    def test_api_logout(self, api_client):
        api_client.login_user()
        r = api_client.get('security_controller.logout')
        assert r.status_code == 204
        assert isinstance(current_user._get_current_object(), AnonymousUser)
