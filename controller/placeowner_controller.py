from flask import render_template, request, session, flash, send_file, jsonify, url_for
from werkzeug.utils import redirect
import os
import requests
from http import HTTPStatus

# custom modules
from config import API_URL
from controller.admin_controller import auth


def register_page():
    print("placeowner register page rendered")
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["pass"]
        
        try:
            auth.create_user_with_email_and_password(request.form['email'], request.form['pass'])
        except Exception as error:
            flash(f"Error occured", error)
            print(error)
            return render_template("signup.html")

        user = auth.sign_in_with_email_and_password(request.form['email'], request.form['pass'])

        user_data = {
            "user_name":name,
            "user_id":user["localId"],
            "email":email,
            "user_type":"place_owner" # normal, place_owner, admin
        }


        response = requests.post(f'{API_URL}/AddUser', json=user_data) #TODO: add url
        status = response.json()['StatusCode']

        if status == HTTPStatus.OK:
            flash("Placeowner added successfully", "success")
        elif status == HTTPStatus.NOT_ACCEPTABLE:
            flash("Error! Same email. Status Code:", HTTPStatus.NOT_ACCEPTABLE)
        else:
            flash("Error! Failed to placeowner user. Internal Server Error Status Code:",HTTPStatus.INTERNAL_SERVER_ERROR)

        return render_template("login.html")
    else:
        return render_template("signup.html")


def login_placeowner_page():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["pass"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            response = requests.get(f'{API_URL}/GetUserInfo?user_id={user["localId"]}')
            res_user_type = response.json()["Data"]["user_type"]
            if res_user_type != "place_owner":
                raise ""
            
            session["user_type"] = res_user_type
            session["is_logged_in"] = True
            session["email"] = user["email"]
            session["uid"] = user["localId"]
            
            status = response.json()['StatusCode']

            if status == HTTPStatus.OK:
                flash("Placeowner added successfully", "success")
                return render_template("list_places.html")    
            else:
                flash("Error! Failed to placeowner user. Internal Server Error Status Code:", HTTPStatus.INTERNAL_SERVER_ERROR)

            return render_template("login.html")       
        except Exception as error:
            flash(f"Error occured", error)
            print(error)
            return render_template("login.html")
    else:
        return render_template("login.html")
    


        