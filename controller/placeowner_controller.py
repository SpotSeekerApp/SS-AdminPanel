from flask import render_template, request, session, flash, send_file, jsonify, url_for
from werkzeug.utils import redirect
import os
import requests
from http import HTTPStatus
from flask_login import login_user

# custom modules
from config import API_URL
from web_api_admin import Admin, OtherUsers
from model.user import User

def register_page():
    print("placeowner register page rendered")
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["pass"]
        
        try:
            user, response = User.add_user_to_db(email, password, name, "place_owner")

            status = response.json()['StatusCode']
            if status == HTTPStatus.OK:
                pass
            elif status == HTTPStatus.NOT_ACCEPTABLE:
                flash("Error! Same email. Status Code:", HTTPStatus.NOT_ACCEPTABLE)
            else:
                flash("Error! Failed to placeowner user. Internal Server Error Status Code:",HTTPStatus.INTERNAL_SERVER_ERROR)

            return render_template("login.html")
    
        except Exception as error:
            flash(f"Error occured", error)
            print(error)
            return render_template("signup.html")

    else:
        return render_template("signup.html")


def login_placeowner_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pass"]
        try:
            user, response = User.sign_in_to_app(email, password, "place_owner")

            status = response.json()['StatusCode']
            if status == HTTPStatus.OK:
                pass
            else:
                flash("Error! Failed to placeowner user. Internal Server Error Status Code:", HTTPStatus.INTERNAL_SERVER_ERROR)
                return render_template("login.html")    

            session["user_type"] = "place_owner"
            session["is_logged_in"] = True
            session["email"] = user["email"]
            session["uid"] = user["localId"]

            status = response.json()['StatusCode']
            response_json = response.json()["Data"]
            user = User(user_id=response_json["user_id"], username=response_json["user_name"], user_email=response_json["email"], user_type=response_json["user_type"])
            login_user(user, remember=True)


            return render_template("placeowner.html")       
        except Exception as error:
            flash(f"Error occured {error}", error)
            print(error)
            return render_template("login.html")
    else:
        return render_template("login.html")
    


        