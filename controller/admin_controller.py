from flask import render_template, request, session, flash, send_file, jsonify, url_for
from werkzeug.utils import redirect
import requests
from http import HTTPStatus
import pyrebase
from flask_login import login_required

# custom modules
from model.user import User
from model.place import Place
from controller.common_controller import auth 
from config import API_URL

@login_required
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

@login_required
def list_users_page():
    response = requests.get(f'{API_URL}/GetAllUsers')
    user_dict = response.json()['Data']
    status = response.json()['StatusCode']
    return render_template("list_users.html", users=user_dict.values())

@login_required
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

@login_required
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
