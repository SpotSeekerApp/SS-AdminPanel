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
from services.user_auth import Admin
from services.logger import logger

@login_required
def update_users_page(): #TODO: decide on columns
    user_data = User(user_id=request.form.get('user_id'),
                      username=request.form.get('user_name'),
                      user_email=request.form['email'],
                      user_password=None).to_json()
    
    logger.info(f"Update user user_id:{session['uid']}, user:{user_data}")

    response = requests.post(f'{API_URL}/UpdateUser', json=user_data) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get(f'{API_URL}/GetAllUsers')

    if status == HTTPStatus.OK:
        msg = f"User edited successfully"
        logger.info(msg)
        flash(msg)
    else:
        msg = f"Error failed to edit user {HTTPStatus.INTERNAL_SERVER_ERROR}"
        logger.error(msg)
        flash(msg)

    return redirect(url_for("list_users_page"))

@login_required
def list_users_page():
    logger.info(f"List users user_id:{session['uid']}")

    response = requests.get(f'{API_URL}/GetAllUsers')
    user_dict = response.json()['Data']
    return render_template("list_users.html", users=user_dict.values())

@login_required
def create_users_page(): #TODO: decide on columns
    logger.info(f"Add user user_id:{session['uid']}")

    try:
        user, response = User.add_user_to_db(request.form.get('email'), request.form.get('password'), request.form.get('user_name'), request.form.getlist('userType')[0])
        status = response.json()['StatusCode']
        if status == HTTPStatus.OK:
            msg = f"User added successfully"
            logger.info(msg)
            flash(msg)
        else:
            msg = f"Error failed to add user {HTTPStatus.INTERNAL_SERVER_ERROR}"
            logger.error(msg)
            flash(msg)

        return redirect(url_for("list_users_page"))
    
    except:
        msg = f"User could not registered"
        logger.info(msg)
        flash(msg)
    
        return redirect(url_for("list_users_page"))

@login_required
def delete_users_page(user_id):
    user_data = User(user_id=user_id).to_json()

    logger.info(f"Delete user user_id:{session['uid']}, user:{user_data}")

    Admin.remove_user(user_id)
    response = requests.post(f'{API_URL}/RemoveUser', json=user_data) #TODO: add url
    status = response.json()['StatusCode']
    response = requests.get(f'{API_URL}/GetAllUsers')

    if status == HTTPStatus.OK:
        msg = f"User deleted successfully"
        logger.info(msg)
        flash(msg)
    else:
        msg = f"Error failed to delete user {HTTPStatus.INTERNAL_SERVER_ERROR}"
        logger.error(msg)
        flash(msg)

    return redirect(url_for("list_users_page"))
