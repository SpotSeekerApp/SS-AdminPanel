import pytest
from unittest.mock import patch, Mock
from services.user_auth import Admin 

# Mock for firebase_admin.auth
firebase_auth_mock = Mock()

@pytest.fixture
def admin():
    return Admin

@patch("firebase_admin.auth.create_user")
def test_add_user_success(mock_auth, admin):
    mock_auth.return_value = Mock(uid='123456')
    
    result_code, user = admin.add_user('test@example.com', 'password')
    
    assert result_code == 0
    assert user.uid == '123456'

def test_add_user_failure(admin):
    firebase_auth_mock.create_user.side_effect = Exception('Creation failed')
    
    result_code, msg = admin.add_user('test@example.com', 'password')
    
    assert result_code == -1
    assert 'Cannot create new user' in msg

