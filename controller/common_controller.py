from flask import render_template, request, session, flash, send_file, jsonify, url_for
from werkzeug.utils import redirect
import requests
from http import HTTPStatus
import pyrebase
from flask_login import login_required


# custom modules
from model.user import User
from model.place import Place
from config import API_URL

# Configuration for Firebase
import firebase_config
firebase_config = firebase_config.config

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)

# Get reference to the auth service and database service
auth = firebase.auth()

@login_required
def list_places_page():
    res_user_type = session["user_type"]

    if res_user_type == "place_owner":
        user_id = session["uid"]
        response = requests.get(f'{API_URL}/GetAllPlaces?user_id={user_id}')
    else:
        response = requests.get(f'{API_URL}/GetAllPlaces')

    place_dict = response.json()['Data']
    status = response.json()['StatusCode']
    print(place_dict.values())

    return render_template("list_places.html", places=place_dict.values())

@login_required
def update_places_page():
    place_data = Place(place_name=request.form['name'],
                      main_category=request.form['main_category'],
                      tags=request.form['tags'],
                      link=request.form['link'],
                      user_id=session["uid"]).to_json()
    
    
    response = requests.post(f'{API_URL}/UpdatePlace', json=place_data) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get(f'{API_URL}/GetAllPlaces')

    if status == HTTPStatus.OK:
        flash("Place edited successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        flash({"error": "Same email"}, HTTPStatus.NOT_ACCEPTABLE)
    else:
        flash({"error": "Failed to edit place"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    return redirect(url_for("list_places_page"))

@login_required
def create_places_page():  #TODO: decide on columns
    place_data = Place(place_name=request.form['name'],
                    main_category=request.form['main_category'],
                    tags=request.form['tags'],
                    link=request.form['link'],
                    user_id=session["uid"]).to_json()

    response = requests.post(f'{API_URL}/AddPlace', json=place_data) #TODO: add url
    status = response.json()['StatusCode']

    if status == HTTPStatus.OK:
        flash("Place added successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        pass
    else:
        flash("Error! Failed to add place. Internal Server Error Status Code:",HTTPStatus.INTERNAL_SERVER_ERROR)

    return redirect(url_for("list_places_page"))


@login_required
def delete_places_page(place_id):
    place_data = Place(place_id=place_id).to_json()
    response = requests.post(f'{API_URL}/RemovePlace', json=place_data) #TODO: add url
    print(response)
    status = response.json()['StatusCode']
    response = requests.get(f'{API_URL}/GetAllPlaces')

    if status == HTTPStatus.OK:
        flash("Place deleted successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        pass
    else:
        flash({"error": "Failed to remove place"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    return redirect(url_for("list_places_page"))
