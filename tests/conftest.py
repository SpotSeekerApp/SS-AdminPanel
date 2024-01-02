import pytest
from app import create_app
import config

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def admin_login(self, email=config.ADMIN_EMAIL, password=config.ADMIN_PASSWORD):
        return self._client.post(
            '/',
            data={'email': email, 'password': password}
        )

    def place_owner_login(self, email=config.PO_EMAIL, password=config.PO_PASSWORD):
        return self._client.post(
            '/login-placeowner',
            data={'email': email, 'pass': password}
        )
    
    def place_owner_register(self, email=config.PO_EMAIL, password=config.PO_PASSWORD):
        return self._client.post(
            '/register',
            data={'name': "test_po", 'email': email, 'pass': password}
        )

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)