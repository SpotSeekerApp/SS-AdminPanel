from flask import render_template, request, session, flash, send_file, jsonify, url_for
from werkzeug.utils import redirect
import requests
from http import HTTPStatus
import pyrebase


# custom modules
from model.user import User
from model.place import Place

# Configuration for Firebase
import firebase_config
firebase_config = firebase_config.config

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)

# Get reference to the auth service and database service
auth = firebase.auth()

def list_users_page():
    response = requests.get('http://localhost:8080/GetAllUsers')
    user_dict = response.json()['Data']
    status = response.json()['StatusCode']
    print(user_dict.values())

    return render_template("list_users.html", users=user_dict.values())

def list_places_page():
    res_user_type = session["user_type"]

    if res_user_type == "place_owner":
        user_id = session["uid"]
        response = requests.get(f'http://localhost:8080/GetAllPlaces?user_id={user_id}')
    else:
        response = requests.get(f'http://localhost:8080/GetAllPlaces')

    place_dict = response.json()['Data']
    status = response.json()['StatusCode']
    print(place_dict.values())

    return render_template("list_places.html", places=place_dict.values())

def create_users_page(): #TODO: decide on columns
    # if request.method == "POST":
    #     result = request.form
    #     email = result["email"]
    #     password = result["pass"]
    #     name = result["name"]
    #     if not password:
    #         print("Password does not meet strength requirements")
    #         return redirect(url_for('signup'))
    #     try:
    #         # Create user account
    #         auth.create_user_with_email_and_password(email, password)
    #         # Authenticate user
    #         user = auth.sign_in_with_email_and_password(email, password)
    #         session["is_logged_in"] = True
    #         session["email"] = user["email"]
    #         session["uid"] = user["localId"]
    #         session["name"] = name
    #         # Save user data
    #         data = {"name": name, "email": email, "last_logged_in": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
    #         # db.child("users").child(session["uid"]).set(data)
    #         return redirect(url_for('welcome'))
    #     except Exception as e:
    #         print("Error occurred during registration: ", e)
    #         return redirect(url_for('signup'))
    # else:
    #     # If user is logged in, redirect to welcome page
    #     if session.get("is_logged_in", False):
    #         return redirect(url_for('welcome'))
    #     else:
    #         return redirect(url_for('signup'))
























    a = request.form
    print(request.form['email'])
    user_data = User(user_id=None,
                    username=request.form['username'],
                    user_email=request.form['email'],
                    user_password="1234").to_json()
    
    print(user_data)
    try:
        auth.create_user_with_email_and_password(request.form['email'], request.form['password'])
        # Authenticate user
        user = auth.sign_in_with_email_and_password(request.form['email'], request.form['password'])
        session["is_logged_in"] = True
        session["email"] = user["email"]
        session["uid"] = user["localId"]
        session["name"] = request.form['username']
    except:
        return redirect(url_for("list_users_page"))

    user_data = {
        "user_name":request.form['username'],
        "user_id":user["localId"],
        "email":user["email"],
        "user_type":"normal" # normal, place_owner, admin
    }


    response = requests.post('http://localhost:8080/AddUser', json=user_data) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get('http://localhost:8080/GetAllUsers')

    if status == HTTPStatus.OK:
        flash("User added successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        flash("Error! Same email. Status Code:", HTTPStatus.NOT_ACCEPTABLE)
    else:
        flash("Error! Failed to add user. Internal Server Error Status Code:",HTTPStatus.INTERNAL_SERVER_ERROR)

    return redirect(url_for("list_users_page"))


def update_users_page(): #TODO: decide on columns
    user_data = User(user_id=request.form.get('user_id'),
                      username=request.form.get('user_name'),
                      user_email=request.form['email'],
                      user_password=None).to_json()

    response = requests.post('http://localhost:8080/UpdateUser', json=user_data) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get('http://localhost:8080/GetAllUsers')

    if status == HTTPStatus.OK:
        flash("User edited successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        flash({"error": "Same email"}, HTTPStatus.NOT_ACCEPTABLE)
    else:
        flash({"error": "Failed to edit user"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    return redirect(url_for("list_users_page"))


def create_places_page():  #TODO: decide on columns
    place_data = Place(place_name=request.form['name'],
                      main_category=request.form['main_category'],
                      tags=request.form['tags'],
                      link=request.form['link']).to_json()

    response = requests.post('http://localhost:8080/AddPlace', json=[place_data]) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get('http://localhost:8080/GetAllPlaces')

    if status == HTTPStatus.OK:
        flash("Place added successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        pass
    else:
        flash("Error! Failed to add place. Internal Server Error Status Code:",HTTPStatus.INTERNAL_SERVER_ERROR)

    return redirect(url_for("list_users_page"))


def update_places_page():
    place_data = Place(place_name=request.form['name'],
                      main_category=request.form['main_category'],
                      tags=request.form['tags'],
                      link=request.form['link']).to_json()
    
    
    response = requests.post('http://localhost:8080/UpdatePlace', json=[place_data]) #TODO: add url
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
    user_data = User(user_id=user_id).to_json()

    response = requests.post('http://localhost:8080/RemoveUser', json=user_data) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get('http://localhost:8080/GetAllUsers')

    if status == HTTPStatus.OK:
        flash("User deleted successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        flash({"error": "Same email"}, HTTPStatus.NOT_ACCEPTABLE)
    else:
        flash({"error": "Failed to remove user"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    return redirect(url_for("list_users_page"))


def delete_places_page():
    place_data = Place(place_name=request.form['name'],
                      main_category=request.form['main_category'],
                      tags=request.form['tags'],
                      link=request.form['link']).to_json()

    response = requests.post('http://localhost:8080/RemovePlace', json=[place_data]) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get('http://localhost:8080/GetAllPlaces')

    if status == HTTPStatus.OK:
        flash("Place deleted successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        pass
    else:
        flash({"error": "Failed to remove place"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    return redirect(url_for("list_places_page"))
