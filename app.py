from flask import Flask, render_template, request, session, flash
from datetime import datetime 
import os
from werkzeug.utils import redirect
# custom modules
import utils, views
import config
import requests

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'

def logout_page():
    if session is not None:
        session.clear()
    
    return redirect("/")

def main_page():
   api_url = 'url'
   response = requests.get(api_url)
   
   if response.status_code == 200:
       data = response.json()
       return redirect("/index", data=data)
   else:
       return f"Failed to fetch data from api. Status code: {response.status_code}"


app.add_url_rule("/", view_func=views.main_page, methods=["GET", "POST"]) # main page 

app.add_url_rule("/register", view_func=views.register_page, methods=["GET", "POST"])
app.add_url_rule("/login-placeowner", view_func=views.login_placeowner_page, methods=["GET", "POST"])

app.add_url_rule("/logout", view_func=logout_page)

app.add_url_rule("/admin", view_func=views.admin_page)
app.add_url_rule("/list-users", view_func=views.list_users_page, methods=["GET", "POST"])
app.add_url_rule("/list-places", view_func=views.list_places_page, methods=["GET", "POST"])
app.add_url_rule("/create-users", view_func=views.create_users_page, methods=["GET", "POST"])
app.add_url_rule("/create-places", view_func=views.create_places_page, methods=["GET", "POST"])
app.add_url_rule("/edit-users/<user_id>", view_func=views.edit_users_page, methods=["GET", "POST"])
app.add_url_rule("/edit-places", view_func=views.edit_places_page, methods=["GET", "POST"])
app.add_url_rule("/delete-users", view_func=views.delete_users_page, methods=["GET", "POST"])
app.add_url_rule("/delete-places", view_func=views.delete_places_page, methods=["GET", "POST"])

if __name__ == "__main__":

    app.run(host=config.localhost_ip,port=config.WEB_PORT, debug=True)    
