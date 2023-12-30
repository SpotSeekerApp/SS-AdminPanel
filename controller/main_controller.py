from flask import render_template, request, session, flash
from http import HTTPStatus
from flask_login import login_user, login_required, logout_user

# custom modules
from services.logger import logger
from model.user import User
import re 

def check_password_strength(password):
    # At least one lower case letter, one upper case letter, one digit, one special character, and at least 8 characters long
    return re.match(r'^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,}$', password) is not None

def main_page():
    if request.method == "POST":
        logger.info("main_page POST request")

        result = request.form
        email = result["email"]
        password = result["password"]
        try:
            user, response = User.sign_in_to_app(email, password, "admin")
            status = response.json()['StatusCode']
            if status == HTTPStatus.OK:
                pass
            else:
                flash("Error! Failed for logging in admin. Internal Server Error Status Code:", HTTPStatus.INTERNAL_SERVER_ERROR)
                return render_template("login.html")    

            session["user_type"] = "admin"
            session["is_logged_in"] = True
            session["email"] = user["email"]
            session["uid"] = user["localId"]

            
            response_json = response.json()["Data"]
            user = User(user_id=response_json["user_id"], username=response_json["user_name"], user_email=response_json["email"], user_type=response_json["user_type"])
            login_user(user, remember=True)

            if status == HTTPStatus.OK:
                logger.info("Admin logged in successfully")
                return render_template("index.html")     
            else:
                msg = f"Error! Failed to login. Internal Server Error Status Code: {HTTPStatus.INTERNAL_SERVER_ERROR}"
                logger.error(msg)
                flash(msg)
                return render_template("index.html")
            
        except Exception as e:
            msg = f"Error occurred. {e}"
            logger.exception(msg)
            flash(msg)
            return render_template("index.html")
        
    else:
        logger.info("main_page GET request")

        return render_template("index.html")

@login_required
def logout_page():
    logger.info(f"User logout user_id:{session['uid']}")

    logout_user()
    if session is not None:
        session.clear()
    
    return render_template("index.html")
