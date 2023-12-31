import pytest
from app import app
from model.user import User
from unittest.mock import patch

def test_config():
    assert not app.testing

@pytest.fixture
def mock_user():
    user = User()
    user.id = 1
    user.name = "Test User"
    return user

def test_main_page(client):
    response = client.get("/")
    assert response.status_code == 200

def test_login_page(client):
    response = client.get("/login-placeowner")
    assert response.status_code == 200

def test_unauthorized(client):
    response = client.get("/list-users")
    assert response.status_code == 200

def test_logout(client):
    response = client.get("/logout")
    assert response.status_code in [200, 302]

