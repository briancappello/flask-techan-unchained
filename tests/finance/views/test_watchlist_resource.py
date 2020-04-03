import pytest

from flask_unchained import url_for


class TestWatchlistResource:
    def test_create(self, api_client, user):
        api_client.login_user()
        r = api_client.post(url_for('watchlist_resource.create'), data=dict(
            name='hi',
        ))
        print(r.json)
