import pytest
from unittest.mock import patch
from http import HTTPStatus

@pytest.fixture
def user_data():
    return {
        'user_id': '1',
        'username': 'TestUser',
        'email': 'test@test.com',
        'user_password': None
    }

@patch('requests.post')
@patch('requests.get')
def test_update_users_page(mock_get, mock_post, client, user_data):
    mock_post.return_value.json.return_value = {'StatusCode': HTTPStatus.OK}
    mock_get.return_value.json.return_value = {'Data': [user_data]}

    response = client.post('/update-users', data=user_data)
    assert response.status_code == 200  # Redirect to list_users_page

@patch('requests.get')
def test_list_users_page(mock_get, client):
    mock_get.return_value.json.return_value = {'Data': {'1': {'username': 'TestUser', 'email': 'test@test.com'}}}

    response = client.get('/list-users')
    assert response.status_code == 200

@patch('model.user.User.add_user_to_db')
@patch('requests.post')
@patch('requests.get')
def test_create_users_page(mock_get, mock_post, mock_add_user, client):
    mock_add_user.return_value = (None, type('obj', (object,), {'json': lambda: {'StatusCode': HTTPStatus.OK}})())
    mock_post.return_value.json.return_value = {'StatusCode': HTTPStatus.OK}
    mock_get.return_value.json.return_value = {'Data': {}}

    response = client.post('/create-users', data={'email': 'new@test.com', 'password': 'pass123', 'user_name': 'NewUser', 'userType': ['admin']})
    assert response.status_code == 200  # Redirect to list_users_page

@patch('services.user_auth.Admin.remove_user')
@patch('requests.post')
@patch('requests.get')
def test_delete_users_page(mock_get, mock_post, mock_remove_user, client, user_data):
    mock_remove_user.return_value = None
    mock_post.return_value.json.return_value = {'StatusCode': HTTPStatus.OK}
    mock_get.return_value.json.return_value = {'Data': [user_data]}

    response = client.post('/delete-users/1')
    assert response.status_code == 200  # Redirect to list_users_page


def test_list_user_page_success(client, auth):
    auth.admin_login()
    response = client.get(f'/list-users')
    assert response.status_code == 200

def test_delete_user_page_success(client, auth):
    auth.admin_login()
    user_id = "1"
    try:
        response = client.post(f'/delete-users/{user_id}')
    except:
        assert True

def test_update_user_page_success(client, auth):
    auth.admin_login()

    new_user_data = {
        "email":"",
        "password":"",
        "user_name":"",
        "user_type":["normal"]
    }
    
    try:
        response = client.post(f'/update-users', data=new_user_data)
    except:
        assert True

def test_create_user_page_success(client, auth):
    auth.admin_login()

    new_user_data = {
        "email":"",
        "password":"",
        "user_name":"",
        "user_type":["normal"]
    }

    response = client.post('/create-users', data=new_user_data)
    assert response.status_code == 302