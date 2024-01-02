import pytest
from unittest.mock import patch
from http import HTTPStatus
from flask import url_for

@pytest.fixture
def place_data():
    return {
        'place_id': '1',
        'place_name': 'Test Place',
        'main_category': 'Category',
        "tags": "wifi,outdoor",
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


def test_update_places_page_success(client, auth):
    # Log in as place owner
    place_data = {
        "place_id": "123",
        "name": "Test Place",
        "main_category": "Cafe",
        "tags": "wifi,outdoor",
        "link": "http://testplace.com"
    }

    auth.place_owner_login()

    # Make a POST request to the update_places_page endpoint
    response = client.post('/update-places', data=place_data)

    # Check if redirect happened to list_places_page
    assert response.status_code == HTTPStatus.FOUND

def test_create_places_page_s(client, auth):
    # Log in as a user (assuming place_owner_login is correct for this case)
    auth.place_owner_login()

    # Mock data for creating a new place
    new_place_data = {
        "name": "New Test Place",
        "main_category": "Restaurant",
        "tags": "family-friendly,outdoor",
        "link": "http://newtestplace.com"
    }

    # Make a POST request to the create_places_page endpoint
    response = client.post('/create-places', data=new_place_data)

    # Check if redirect happened to list_places_page
    assert response.status_code == HTTPStatus.FOUND


def test_delete_places_page_s(client, auth):
    # Log in as a user (assuming place_owner_login is correct for this case)
    auth.place_owner_login()

    user_id = "1"

    # Make a POST request to the create_places_page endpoint
    response = client.post(f'/delete-places/{user_id}')

    # Check if redirect happened to list_places_page
    assert response.status_code == HTTPStatus.FOUND