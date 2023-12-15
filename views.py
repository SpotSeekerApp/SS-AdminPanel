from flask import render_template, request, session, flash, send_file, jsonify
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

def register_page():
    conn = None
    try:
        conn = dbapi.connect(config.DSN)
        cur = conn.cursor()
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            password_conf = request.form["password_conf"]

            if (not email
                or not password
            ):
                flash("Please fill in all necessary information")
                return render_template("register.html")
            if len(password) < 6:
                flash("Password length should be at least 6")
                return render_template("register.html")
            if password != password_conf:
                flash("Password matching failed")
                return render_template("register.html")

            st = f"SELECT * FROM placeowners WHERE email='{email}'"
            cur.execute(st)
            fetchedUser = cur.fetchone()
            if not ((fetchedUser is None)):
                flash("There is already an existing account with this email")
                return render_template("register.html")

            cur.execute(
                "INSERT INTO placeowners (email, \
                            password)\
                            VALUES (%s, %s);",
                (email, password),
            )

            flash("Successfully registered")

            return redirect("/login-placeowner")
        else:
            return render_template("register.html")
    except dbapi.errors.UniqueViolation:
        flash("You are already registered.")
        return render_template("register.html")
    except os.error:
        utils.err_handler(os.error)
        return "Something happened"
    finally:
        cur.close()
        conn.commit()
        conn.close()

def login_placeowner_page():
    conn = dbapi.connect(config.DSN)
    try:
        cur = conn.cursor()
        if request.method == "POST":
            if "id" in session.keys():
                flash("You are already logged in")
                return render_template("login_placeowner.html")
            
            email = request.form["email"]
            password = request.form["password"]

            # check if user is a placeowner
            query = f"SELECT email FROM placeowners WHERE email='{email}'"
            print(query)
            cur.execute(query) 
            fetchedplaceowner = cur.fetchone() 

            # if placeowner with corresponding email doesn't exist, render page warning message 
            if (fetchedplaceowner is None):
                flash("Invalid email")
                return render_template("login_placeowner.html") 
            
            # if placeowner found with corresponding email, fetch password of the placeowner from database     
            query = f"SELECT id, email, password FROM placeowners WHERE email='{email}' and password='{password}'"
            cur.execute(query) 

            fetched = cur.fetchone()

            # validate password by comparing fetched password information from database with input password 
            id, email, password_t = fetched
            if password_t != password: # if password is invalid, render page with warning message 
                flash("Invalid Password")
                return render_template("login_placeowner.html")

            session["loggedin"] = True
            session["id"] = id
            session["email"] = email
            session["isplaceowner"] = False if fetchedplaceowner == None else True
        
            conn.commit()
            conn.close()
            return redirect("/")
        else:
            return render_template("login_placeowner.html")
        
    except dbapi.errors.UniqueViolation:
        flash("You are already logged in")
        return render_template("login_placeowner.html")
    except os.error:
        flash("Something happened")
        return render_template("login_placeowner.html")

def main_page():
    conn = dbapi.connect(config.DSN)
    try:
        cur = conn.cursor()
        if request.method == "POST":
            if "id" in session.keys():
                flash("You are already logged in")
                return render_template("index.html")
            
            email = request.form["email"]
            password = request.form["password"]

            # check if user is an Admin 
            query = f"SELECT email FROM admins WHERE email='{email}'"
            cur.execute(query) 
            fetchedAdmin = cur.fetchone() 

            # if admin with corresponding email doesn't exist, render page warning message 
            if (fetchedAdmin is None):
                flash("Invalid email")
                return render_template("index.html") 
            
            # if admin found with corresponding email, fetch password of the admin from database     
            query = f"SELECT admin_id, adminname, email, password FROM admins WHERE email='{email}' and password='{password}'"
            cur.execute(query) 

            fetched = cur.fetchone()
            # validate password by comparing fetched password information from database with input password 
            id, email, password_t = fetched
            if password_t != password: # if password is invalid, render page with warning message 
                flash("Invalid Password")
                return render_template("index.html")

            session["loggedin"] = True
            session["id"] = id
            session["email"] = email
            session["isadmin"] = False if fetchedAdmin == None else True
        
            conn.commit()
            conn.close()
            return redirect("/")
        else:
            return render_template("index.html")
    except dbapi.errors.UniqueViolation:
        flash("You are already logged in")
        return render_template("index.html")
    except os.error:
        flash("Something happened")
        return render_template("index.html")
    

def access_denied():
    return render_template("access-denied.html")

def admin_page():
    return render_template("admin.html")



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

def placeowner_page():
    global dummy_places
    return render_template("placeowner.html", places=dummy_places)

def list_users_page():
    response = requests.get('http://localhost:8080/GetAllUsers')
    user_dict = response.json()['Data']
    status = response.json()['StatusCode']
    print(user_dict.values())

    return render_template("list_users.html", users=user_dict.values())
    
def list_places_page():
    global dummy_places
    return render_template("list_places.html", places = dummy_places)

api_url = "http://localhost:8080"

def get_users():
    response = requests.get('http://localhost:8080/GetAllUsers')
    #print(response)

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

    return render_template("list_users.html", users=user_dict.values())

def update_users_page(): #TODO: decide on columns
    #print(user_id)
    # user_id = request.form.get('user_id')
    user_id = request.form['user_id']
    print(request.form) 
    user_data =  {
        "user_id" : user_id,
        "user_name" : request.form['user_name'],
        "email": request.form['email'],
    }
    
    response = requests.post('http://localhost:8080/UpdateUser', json=user_data) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get('http://localhost:8080/GetAllUsers')
    user_dict = response.json()['Data']
    users_list_status = response.json()['StatusCode']

    if status == HTTPStatus.OK:
        flash("User added successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        flash({"error": "Same email"}, HTTPStatus.NOT_ACCEPTABLE)
    else:
        print(user_data)
        flash({"error": "Failed to add user"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    return render_template("list_users.html", users=user_dict.values())

def create_places_page():  #TODO: decide on columns
    
    place_data = [
        {
        "place_name": request.form['place_name'],
        "location": request.form['location'],
        "photo_link": request.form['link'],
        "phone_number": request.form['phone_number']
        }
    ]

    response = requests.post(api_url, json=place_data) #TODO: add url

    if response.status_code == HTTPStatus.OK:
        flash("User added successfully", "success")
    else:
        return jsonify({"error": "Failed to add place"}), HTTPStatus.INTERNAL_SERVER_ERROR
    

#def edit_users_page():
#    return render_template("edit_user.html")

def edit_places_page():
    return render_template("edit_place.html")

def delete_users_page():
    return render_template("edit_user.html")

def delete_places_page():
    return render_template("edit_place.html")

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Save Changes')


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