from flask import render_template, request, session, flash, send_file, jsonify, url_for
from werkzeug.utils import redirect
import requests
from http import HTTPStatus
import pyrebase

# custom modules
from model.user import User
from model.place import Place
from controller.common_controller import auth 
from config import API_URL

def update_users_page(): #TODO: decide on columns
    user_data = User(user_id=request.form.get('user_id'),
                      username=request.form.get('user_name'),
                      user_email=request.form['email'],
                      user_password=None).to_json()

    response = requests.post(f'{API_URL}/UpdateUser', json=user_data) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get(f'{API_URL}/GetAllUsers')

    if status == HTTPStatus.OK:
        flash("User edited successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        flash({"error": "Same email"}, HTTPStatus.NOT_ACCEPTABLE)
    else:
        flash({"error": "Failed to edit user"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    return redirect(url_for("list_users_page"))

def list_users_page():
    response = requests.get(f'{API_URL}/GetAllUsers')
    user_dict = response.json()['Data']
    status = response.json()['StatusCode']
    return render_template("list_users.html", users=user_dict.values())


def create_users_page(): #TODO: decide on columns

    try:
        auth.create_user_with_email_and_password(request.form.get('email'), request.form.get('password'))
        # Authenticate user
        user = auth.sign_in_with_email_and_password(request.form.get('email'),request.form.get('password'))
    
        selected_options = request.form.getlist('userType')
        user_data = User(user_id=user["localId"],
                      username=request.form.get('user_name'),
                      user_email=request.form.get('email'),
                      user_password=None,
                      user_type=selected_options[0]).to_json()
        
        print("user_data",user_data)
        response = requests.post(f'{API_URL}/AddUser', json=user_data) #TODO: add url
        status = response.json()['StatusCode']
        response = requests.get(f'{API_URL}/GetAllUsers')

        if status == HTTPStatus.OK:
           flash("User added successfully", "success")
        elif status == HTTPStatus.NOT_ACCEPTABLE:
           flash("Error! Same email. Status Code:", HTTPStatus.NOT_ACCEPTABLE)
        else:
           flash("Error! Failed to add user. Internal Server Error Status Code:",HTTPStatus.INTERNAL_SERVER_ERROR)
    
        return redirect(url_for("list_users_page"))
    except:
        flash("User couldnt registered:")
        return redirect(url_for("list_users_page"))

def delete_users_page(user_id):
    print("user_id", user_id)
    user_data = User(user_id=user_id).to_json()
    print("user_data", user_data)
    response = requests.post(f'{API_URL}/RemoveUser', json=user_data) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get(f'{API_URL}/GetAllUsers')

    if status == HTTPStatus.OK:
        flash("User deleted successfully", "success")
    elif status == HTTPStatus.NOT_ACCEPTABLE:
        flash({"error": "Same email"}, HTTPStatus.NOT_ACCEPTABLE)
    else:
        flash({"error": "Failed to remove user"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    return redirect(url_for("list_users_page"))

def admin_login_page():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["pass"]
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
            
            status = response.json()['StatusCode']

            if status == HTTPStatus.OK:
                flash("Admin logged in successfully", "success")
                return render_template("admin.html")     
            else:
                flash("Error! Failed to login. Internal Server Error Status Code:", HTTPStatus.INTERNAL_SERVER_ERROR)
                return render_template("index.html")
            
        except Exception as e:
            print("Error occurred: ", e)
            return render_template("admin.html")
    else:
        return render_template("index.html")
