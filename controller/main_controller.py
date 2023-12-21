from flask import render_template, request, session, flash, send_file, jsonify, url_for
from werkzeug.utils import redirect
import requests
from http import HTTPStatus

# custom modules
import utils
from model.user import User
from model.place import Place
from config import API_URL
from controller.admin_controller import auth


def main_page():
    if request.method == "GET":
        response = requests.get(API_URL)
        # if response.status_code == 200:
        if response.status_code:
            return render_template("index.html")
        else:
            return f"Failed to fetch data from api. Status code: {response.status_code}"
        
    elif request.method == "POST":
        form = request.form
        try:
            user = auth.sign_in_with_email_and_password(form['email'], form['password'])
            response = requests.get(f'{API_URL}/GetUserInfo?user_id={user["localId"]}')
            res_user_type = response.json()["Data"]["user_type"]
            # if res_user_type != "admin":
            #     raise ""
            
            session["user_type"] = res_user_type
            session["is_logged_in"] = True
            session["email"] = user["email"]
            session["uid"] = user["localId"]
            
            status = response.json()['StatusCode']

            if status == HTTPStatus.OK:
                flash("Admin login success.", "success")
            else:
                flash("Error! Failed to admin. Internal Server Error Status Code:", HTTPStatus.INTERNAL_SERVER_ERROR)

            return render_template("admin.html")       
        except Exception as e:
            print("Error occurred: ", e)
            return render_template("index.html")


# def main_page():
#     admin_id = request.form['admin_id']
   
#     response = requests.get(f'http://localhost:8080/ReturnPassword?username={admin_id}') #TODO: add url
#     status = response.json()['StatusCode']
#     encryped_password = response.json()['password']

#     if utils.check_password(encryped_password, request.form['password']):
#         session["loggedin"] = True
#         session["id"] = admin_id
#         session["isadmin"] = True
#         return render_template("admin.html")
#     else:
#         flash("Invalid Password")
#         return render_template("index.html")
    
def logout_page():
    if session is not None:
        session.clear()
    
    return redirect("/")

def access_denied():
    return render_template("access-denied.html")

def admin_page():
    return render_template("admin.html")