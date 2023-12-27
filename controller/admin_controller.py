from flask import render_template, request, session, flash, send_file, jsonify, url_for
from werkzeug.utils import redirect
import requests
from http import HTTPStatus
import pyrebase
from flask_login import login_required

# custom modules
from model.user import User
from model.place import Place
from config import API_URL
from web_api_admin import Admin

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
    return render_template("list_users.html", users=user_dict.values())

@login_required
def create_users_page(): #TODO: decide on columns

    try:
        user, response = User.add_user_to_db(request.form.get('email'), request.form.get('password'), request.form.get('user_name'), request.form.getlist('userType')[0])
        status = response.json()['StatusCode']
        if status == HTTPStatus.OK:
            flash("User added successfully", HTTPStatus.OK)
        elif status == HTTPStatus.NOT_ACCEPTABLE:
            flash("Error! Same email. Status Code:", HTTPStatus.NOT_ACCEPTABLE)
        else:
            flash("Error! Failed to placeowner user. Internal Server Error Status Code:",HTTPStatus.INTERNAL_SERVER_ERROR)

        return redirect(url_for("list_users_page"))
    except:
        flash("User couldnt registered:")
        return redirect(url_for("list_users_page"))

@login_required
def delete_users_page(user_id):
    print("user_id", user_id)
    user_data = User(user_id=user_id).to_json()
    print("user_data", user_data)

    Admin.remove_user(user_id)
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
