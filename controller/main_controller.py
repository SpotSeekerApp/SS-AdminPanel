from flask import render_template, request, session, flash, send_file, jsonify, url_for
from werkzeug.utils import redirect
import requests
from http import HTTPStatus
from urllib import error
import json
from flask_login import login_user

# custom modules
import utils
from model.user import User
from model.place import Place
from config import API_URL
from controller.admin_controller import auth

def main_page():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["password"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            response = requests.get(f'{API_URL}/GetUserInfo?user_id={user["localId"]}')
            res_user_type = response.json()["Data"]["user_type"]
            if res_user_type != "admin":
                flash("You're not admin.")
                return render_template("index.html")
            
            session["user_type"] = res_user_type
            session["is_logged_in"] = True
            session["email"] = user["email"]
            session["uid"] = user["localId"]

            response_json = response.json()["Data"]
            user = User(user_id=response_json["user_id"], username=response_json["user_name"], user_email=response_json["email"], user_type=response_json["user_type"])
            login_user(user, remember=True)
            
            status = response.json()['StatusCode']

            if status == HTTPStatus.OK:
                flash("Admin logged in successfully", "success")
                return render_template("admin.html")     
            else:
                flash("Error! Failed to login. Internal Server Error Status Code:", HTTPStatus.INTERNAL_SERVER_ERROR)
                return render_template("index.html")
            
        except Exception as e:
            print("Error occurred: ", e)
            return render_template("index.html")
    else:
        return render_template("index.html")


def logout_page():
    if session is not None:
        session.clear()
    
    return redirect("/")

def access_denied():
    return render_template("access-denied.html")

def admin_page():
    return render_template("admin.html")

