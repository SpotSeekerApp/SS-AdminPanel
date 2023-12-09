from flask import render_template, request, session, flash, send_file
import psycopg2 as dbapi
from werkzeug.utils import redirect
import os
import pandas as pd 
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


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
    {"id": 1, "username": "user1", "email": "user1@example.com", "password": "password1"},
    {"id": 2, "username": "user2", "email": "user2@example.com", "password": "password2"},
    {"id": 3, "username": "user3", "email": "user3@example.com", "password": "password3"},
]

dummy_places = [
    {"id": 1, "name": "place1", "info": "place info 1", "tags": ["tag1", "tag2"], "reviews": ["review1", "review2"]},
    {"id": 2, "name": "place2", "info": "place info 2", "tags": ["tag1", "tag2"], "reviews": ["review1", "review2"]},
    {"id": 3, "name": "place3", "info": "place info 3", "tags": ["tag1", "tag2"], "reviews": ["review1", "review2"]},
]

def list_users_page():
    global dummy_users
    return render_template("list_users.html", users=dummy_users)
    
def list_places_page():
    global dummy_places
    return render_template("list_places.html", places = dummy_places)

def create_users_page():
    return render_template("create_user.html")

def create_places_page():
    return render_template("create_place.html")

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


#@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
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
        return redirect(url_for("list_users_page"))