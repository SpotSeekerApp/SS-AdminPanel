from flask import render_template, request, session, flash, send_file, jsonify, url_for
import psycopg2 as dbapi
from werkzeug.utils import redirect
import os
import pandas as pd 
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from http import HTTPStatus

# custom modules
import utils
import config


dummy_users = [
    {"id": 1, "username": "user1", "email": "user1@example.com"},
    {"id": 2, "username": "user2", "email": "user2@example.com"},
    {"id": 3, "username": "user3", "email": "user3@example.com"},
]

dummy_places = [
    {"id": 1, "name": "place1", "info": "place info 1", "tags": ["tag1", "tag2"], "reviews": ["review1", "review2"]},
    {"id": 2, "name": "place2", "info": "place info 2", "tags": ["tag1", "tag2"], "reviews": ["review1", "review2"]},
    {"id": 3, "name": "place3", "info": "place info 3", "tags": ["tag1", "tag2"], "reviews": ["review1", "review2"]},
]


def main_page():
    admin_id = request.form['admin_id']
   
    response = requests.get(f'http://localhost:8080/ReturnPassword?username={admin_id}') #TODO: add url
    status = response.json()['StatusCode']
    encryped_password = response.json()['password']

    if utils.check_password(encryped_password, request.form['password']):
        session["loggedin"] = True
        session["id"] = admin_id
        session["isadmin"] = True
        return render_template("admin.html")
    else:
        flash("Invalid Password")
        return render_template("index.html")
    


def register_page():
    
    placeowner_data =  {
        "placeowner_name" : request.form['placeowner_name'],
        "password": request.form['password'],
    }
    
    response = requests.post('http://localhost:8080/AddPlaceowner', json=placeowner_data) #TODO: add url
    status = response.json()['StatusCode']

    if status == HTTPStatus.OK:
        flash("Placeowner added successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        flash("Error! Same email. Status Code:", HTTPStatus.NOT_ACCEPTABLE)
    else:
        flash("Error! Failed to placeowner user. Internal Server Error Status Code:",HTTPStatus.INTERNAL_SERVER_ERROR)

    return render_template("login_placeowner.html")


def login_placeowner_page():
    placeowner_id = request.form['placeowner_id']
   
    response = requests.get(f'http://localhost:8080/ReturnPassword?username={placeowner_id}') #TODO: add url
    status = response.json()['StatusCode']
    encryped_password = response.json()['password']

    if utils.check_password(encryped_password, request.form['password']):
        session["loggedin"] = True
        session["id"] = placeowner_id
        session["isplaceowner"] = True
        return render_template("placeowner.html")
    else:
        flash("Invalid Password")
        return render_template("login_placeowner.html")
        

def access_denied():
    return render_template("access-denied.html")

def admin_page():
    return render_template("admin.html")


def placeowner_page(place_owner_id):
    #global dummy_places
    response = requests.get(f'http://localhost:8080/GetAllPlaces?place_owner_id={place_owner_id}')
    place_dict = response.json()['Data']
    status = response.json()['StatusCode']
    print(place_dict.values())

    return render_template("placeowner.html", places=place_dict.values())

def list_users_page():
    response = requests.get('http://localhost:8080/GetAllUsers')
    user_dict = response.json()['Data']
    status = response.json()['StatusCode']
    print(user_dict.values())

    return render_template("list_users.html", users=user_dict.values())


def list_places_page():
    response = requests.get('http://localhost:8080/GetAllPlaces')
    place_dict = response.json()['Data']
    status = response.json()['StatusCode']
    print(place_dict.values())

    return render_template("list_places.html", places=place_dict.values())


def create_users_page(): #TODO: decide on columns

    user_data =  {
        "user_name" : request.form['username'],
        "email": request.form['email'],
    }
    
    response = requests.post('http://localhost:8080/AddUser', json=user_data) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get('http://localhost:8080/GetAllUsers')
    user_dict = response.json()['Data']
    users_list_status = response.json()['StatusCode']

    if status == HTTPStatus.OK:
        flash("User added successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        flash("Error! Same email. Status Code:", HTTPStatus.NOT_ACCEPTABLE)
    else:
        flash("Error! Failed to add user. Internal Server Error Status Code:",HTTPStatus.INTERNAL_SERVER_ERROR)

    return redirect(url_for("list_users_page"))

def update_users_page(): #TODO: decide on columns
    #print(user_id)
    # user_id = request.form.get('user_id')
    #user_id = request.form['user_id']
    print(request.form.get('user_id')) 
    user_data =  {
        "user_id" : int(request.form.get('user_id')),
        "user_name" : request.form.get('user_name'),
        "email": request.form.get('email'),
    }
    
    response = requests.post('http://localhost:8080/UpdateUser', json=user_data) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get('http://localhost:8080/GetAllUsers')
    user_dict = response.json()['Data']
    users_list_status = response.json()['StatusCode']
    print(user_data)
    if status == HTTPStatus.OK:
        flash("User edited successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        flash({"error": "Same email"}, HTTPStatus.NOT_ACCEPTABLE)
    else:
        flash({"error": "Failed to edit user"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    #return render_template("list_users.html", users=user_dict.values())
    return redirect(url_for("list_users_page"))

def create_places_page():  #TODO: decide on columns
    
    place_data = [
        {
        "place_name": request.form['name'],
        "main_category": request.form['main_category'],
        "tags": request.form['tags'],
        "link": request.form['link']
        }
    ]

    response = requests.post('http://localhost:8080/AddPlace', json=place_data) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get('http://localhost:8080/GetAllPlaces')
    places_dict = response.json()['Data']
    places_list_status = response.json()['StatusCode']

    if status == HTTPStatus.OK:
        flash("User added successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        flash("Error! Same email. Status Code:", HTTPStatus.NOT_ACCEPTABLE)
    else:
        flash("Error! Failed to add user. Internal Server Error Status Code:",HTTPStatus.INTERNAL_SERVER_ERROR)

    return redirect(url_for("list_users_page"))


def update_places_page():
    place_data = [
        {
        "place_name": request.form['name'],
        "main_category": request.form['main_category'],
        "tags": request.form['tags'],
        "link": request.form['link']
        }
    ]
    print(place_data)
    
    response = requests.post('http://localhost:8080/UpdatePlace', json=place_data) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get('http://localhost:8080/GetAllPlaces')
    if status == HTTPStatus.OK:
        flash("Place edited successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        flash({"error": "Same email"}, HTTPStatus.NOT_ACCEPTABLE)
    else:
        flash({"error": "Failed to edit place"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    return redirect(url_for("list_places_page"))


def delete_users_page(user_id):
    user_data =  {
        "user_id" : user_id,
    }

    print(user_data)

    response = requests.post('http://localhost:8080/RemoveUser', json=user_data) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get('http://localhost:8080/GetAllUsers')
    user_dict = response.json()['Data']
    users_list_status = response.json()['StatusCode']
    if status == HTTPStatus.OK:
        flash("User deleted successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        flash({"error": "Same email"}, HTTPStatus.NOT_ACCEPTABLE)
    else:
        flash({"error": "Failed to remove user"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    #return render_template("list_users.html", users=user_dict.values())
    return redirect(url_for("list_users_page"))


def delete_places_page():
    place_data = [
        {
        "place_name": request.form['name'],
        "main_category": request.form['main_category'],
        "tags": request.form['tags'],
        "link": request.form['link']
        }
    ]

    response = requests.post('http://localhost:8080/RemovePlace', json=place_data) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get('http://localhost:8080/GetAllPlaces')
    if status == HTTPStatus.OK:
        flash("Place deleted successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        flash({"error": "Same email"}, HTTPStatus.NOT_ACCEPTABLE)
    else:
        flash({"error": "Failed to remove place"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    return redirect(url_for("list_places_page"))







def edit_users_page(user_id):

    user = dummy_users
    if request.method == "GET":
        values = {"id":"", "username":"","email":"", "password":""}
        return render_template('edit_user.html', user=values)
    else:
        id = request.form["id"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        #update database
        return redirect("list_users.html")
    

def create_placeowner_places(): #TODO: decide on columns

    places_data = [
        {
        "place_name": request.form['place_name'],
        "location": request.form['location'],
        "photo_link": request.form['link'],
        "phone_number": request.form['phone_number']
        },
    ]

    response = requests.post(api_url, json=places_data) #TODO: add url

    if response.status_code == 200:
        flash("Place added successfully", "success")
    else:
        return jsonify({"error": "Failed to add place"}), 500