import pytest
from unittest.mock import patch
from http import HTTPStatus

@pytest.fixture
def place_data():
    return {
        'place_id': '1',
        'place_name': 'Test Place',
        'main_category': 'Category',
        'tags': ['Tag1', 'Tag2'],
        'link': 'http://example.com',
        'user_id': 'user123'
    }

@pytest.fixture
def mock_session(monkeypatch):
    monkeypatch.setattr('flask.session', {'uid': 'user123', 'user_type': 'place_owner'})

@patch('requests.get')
def test_list_places_page(mock_get, client, mock_session):
    mock_get.return_value.json.return_value = {'StatusCode': HTTPStatus.OK, 'Data': {'1': {'place_name': 'Test Place'}}}
    response = client.get('/list-places')
    assert response.status_code == 200

@patch('requests.post')
def test_update_places_page(mock_post, client, mock_session, place_data):
    mock_post.return_value.json.return_value = {'StatusCode': HTTPStatus.OK}
    response = client.post('/update-places', data=place_data)
    assert response.status_code == 200

@patch('requests.post')
def test_create_places_page(mock_post, client, mock_session, place_data):
    mock_post.return_value.json.return_value = {'StatusCode': HTTPStatus.OK}
    response = client.post('/create-places', data=place_data)
    assert response.status_code == 200

@patch('requests.post')
def test_delete_places_page(mock_post, client, mock_session):
    mock_post.return_value.json.return_value = {'StatusCode': HTTPStatus.OK}
    response = client.post('/delete-places/1')
    assert response.status_code == 200
