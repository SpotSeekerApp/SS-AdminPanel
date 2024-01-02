import pytest
from unittest.mock import patch
from http import HTTPStatus
from flask import template_rendered, session

# Helper to capture templates rendered in the view
@pytest.fixture
def captured_templates(app):
    rendered_templates = []

    def record(sender, template, context, **extra):
        rendered_templates.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield rendered_templates
    finally:
        template_rendered.disconnect(record, app)

def test_main_page_get(client, captured_templates):
    response = client.get('/')
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "index.html"


def test_admin_login(client, auth):
    assert client.get('/').status_code == 200
    auth.admin_login()
    with client:
        client.get('/')
        print(session)
        assert session["user_type"] == "admin"

def test_placeowner_login(client, auth):
    assert client.get('/login-placeowner').status_code == 200
    auth.place_owner_login()
    with client:
        client.get('/')
        print(session)
        assert session["user_type"] == "place_owner"


def test_placeowner_register(client, auth):
    assert client.get('/register').status_code == 200
    auth.place_owner_login()
    with client:
        client.get('/')
        print(session)
        assert session["user_type"] == "place_owner"

def test_admin_logout(client, auth):
    auth.admin_login()  # Assuming this sets the session correctly
    with client:
        auth.logout()
        assert 'user_id' not in session

def test_placeowner_logout(client, auth):
    auth.place_owner_login()  # Assuming this sets the session correctly
    with client:
        auth.logout()
        assert 'user_id' not in session

@patch('model.user.User.sign_in_to_app')
def test_main_page_post_valid(mock_sign_in, client, captured_templates):
    mock_sign_in.return_value = ({}, {"json": lambda: {"StatusCode": HTTPStatus.OK, "Data": {"user_id": "1", "user_name": "Test", "email": "test@test.com", "user_type": "admin"}}})
    response = client.post('/', data={'email': 'test@test.com', 'password': 'password'})
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "index.html"

@patch('model.user.User.sign_in_to_app')
def test_main_page_post_invalid(mock_sign_in, client, captured_templates):
    mock_sign_in.side_effect = Exception("Test error")
    response = client.post('/', data={'email': 'test@test.com', 'password': 'invalid'})
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "index.html"

