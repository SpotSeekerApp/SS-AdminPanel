from flask import render_template, request, session, flash, url_for, redirect
from http import HTTPStatus
from flask_login import login_user

# custom modules
from services.user_auth import OtherUsers
from model.user import User
from services.logger import logger
import os, sys


def register_page():
    if request.method == "POST":
        logger.info("placeowner register_page POST request")

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
        except Exception as err:
            msg = f"Error occurred {err}"
            logger.exception(msg)
            flash(msg)
            return render_template("signup.html")

    else:
        logger.info("placeowner register_page GET request")
        return render_template("signup.html")
    

def reset_password_page():
    if request.method == "POST":
        logger.info("placeowner reset_password_page POST request")

        email = request.form["email"]
        try:
            OtherUsers.send_reset_password_mail(email)
            flash("Please check your email address.")
            return render_template("reset_password.html")
        except Exception as e:
            msg = f"Error occurred {e}"
            logger.exception(msg)
            flash(msg)
            return render_template("reset_password.html")  
        
    else:
        logger.info("placeowner reset_password_page GET request")
        return render_template("reset_password.html")


def login_placeowner_page():
    if request.method == "POST":
        logger.info("placeowner login_page POST request")

        email = request.form["email"]
        password = request.form["pass"]
        try:
            user, response = User.sign_in_to_app(email, password, "place_owner")

            status = response.json()['StatusCode']
            if status == HTTPStatus.OK:
                logger.info("Admin logged in successfully")
            else:
                msg = f"Error! Failed to login. Internal Server Error Status Code: {HTTPStatus.INTERNAL_SERVER_ERROR}"
                logger.error(msg)
                flash(msg)
                return render_template("login.html")    

            session["user_type"] = "place_owner"
            session["is_logged_in"] = True
            session["email"] = user["email"]
            session["uid"] = user["localId"]

            status = response.json()['StatusCode']
            response_json = response.json()["Data"]
            user = User(user_id=response_json["user_id"], username=response_json["user_name"], user_email=response_json["email"], user_type=response_json["user_type"])
            login_user(user, remember=True)

            return redirect(url_for("list_places_page"))
        except Exception as e:
            msg = f"Error occurred {e}"
            logger.exception(msg)
            flash(msg)
            return render_template("login.html")
        
    else:
        logger.info("placeowner login_page GET request")

        return render_template("login.html")