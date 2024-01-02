import pytest
from unittest.mock import patch, MagicMock
from model.user import User  # Replace with the correct import path
import config

@patch('requests.post')
def test_add_user_to_db_error(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {'StatusCode': 200}
    mock_post.return_value = mock_response

    # Assuming Admin.add_user() and OtherUsers.sign_in() are already tested elsewhere
    with patch('services.user_auth.Admin.add_user', return_value=(-1, None)), \
         patch('services.user_auth.OtherUsers.sign_in', return_value={"idToken": "token", "localId": "local_id"}):
        try:
            user, response = User.add_user_to_db("test@example.com", "password123", "testuser", "admin")
            assert False
        except Exception:
            assert True


@patch('requests.post')
def test_add_user_to_db_error_2(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {'StatusCode': 200}
    mock_post.return_value = mock_response

    # Assuming Admin.add_user() and OtherUsers.sign_in() are already tested elsewhere
    with patch('services.user_auth.Admin.add_user', return_value=(0, None)), \
         patch('services.user_auth.OtherUsers.sign_in', return_value={"idToken": "token", "localId": "local_id"}), \
         patch('services.user_auth.OtherUsers.send_verification'):
        try:
            user, response = User.add_user_to_db("test@example.com", "password123", "testuser", "admin")
            assert False
        except Exception:
            assert True


@patch('requests.get')
@patch('services.user_auth.OtherUsers.is_verified')
@patch('services.user_auth.OtherUsers.sign_in')
def test_sign_in_to_app(mock_sign_in, mock_is_verified, mock_get):
    # Setup mock returns
    mock_sign_in.return_value = {"localId": "123", "idToken": "token"}
    mock_is_verified.return_value = True

    mock_response = MagicMock()
    mock_response.json.return_value = {"Data": {"user_type": "admin"}}
    mock_get.return_value = mock_response

    # Call the method
    user, response = User.sign_in_to_app("test@example.com", "password123", "admin")

    # Assert calls and responses
    mock_sign_in.assert_called_with("test@example.com", "password123")
    mock_is_verified.assert_called_with("token")
    assert response.json() == {"Data": {"user_type": "admin"}}
    assert user == {"localId": "123", "idToken": "token"}


def test_sign_in_to_app_success():
    user, response = User.sign_in_to_app(config.ADMIN_EMAIL, config.ADMIN_PASSWORD, "admin")
    assert response.json()['StatusCode'] == 200


def test_sign_in_to_app_not_the_same_user_type():
    try:
        User.sign_in_to_app(config.ADMIN_EMAIL, config.ADMIN_PASSWORD, "place_owner")
        assert False
    except Exception:
        assert True

def test_get_user_from_db_success():
    User.get_user_from_db(config.ADMIN_USERID)
    assert True

def test_get_user_from_db_success():
    try:
        User.get_user_from_db("1")
    except Exception:
        assert True