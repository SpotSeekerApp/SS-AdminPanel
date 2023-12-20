from flask import render_template, request, session, flash, send_file, jsonify, url_for
from werkzeug.utils import redirect
import requests
from http import HTTPStatus

# custom modules
import utils
from model.user import User
from model.place import Place

def main_page():
   api_url = 'url'
   response = requests.get(api_url)
   
   if response.status_code == 200:
       data = response.json()
       return redirect("/index", data=data)
   else:
       return f"Failed to fetch data from api. Status code: {response.status_code}"

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