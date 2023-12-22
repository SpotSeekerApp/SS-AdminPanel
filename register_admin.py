from flask import render_template, request, session, flash, send_file, jsonify, url_for
from werkzeug.utils import redirect
import os
import requests
from http import HTTPStatus

# custom modules
import utils
import config
from config import API_URL
from model.user import User

from controller.admin_controller import auth

name = "admin"
email = "zeynepbetulaltundal@gmail.com"
password = "admin123"

auth.create_user_with_email_and_password(email, password)
user = auth.sign_in_with_email_and_password(email, password)

user_data = {
    "user_name":name,
    "user_id":user["localId"],
    "email":email,
    "user_type":"admin" # normal, place_owner, admin
}


response = requests.post(f'{API_URL}/AddUser', json=user_data) #TODO: add url
status = response.json()['StatusCode']

if status == HTTPStatus.OK:
    print("admin added successfully", "success")
elif status == HTTPStatus.NOT_ACCEPTABLE:
    print("Error! Same email. Status Code:", HTTPStatus.NOT_ACCEPTABLE)
else:
    print("Internal Server Error Status Code:",HTTPStatus.INTERNAL_SERVER_ERROR)
