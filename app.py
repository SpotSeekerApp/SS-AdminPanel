from flask import Flask, render_template, request, session, flash
from datetime import datetime 
import os
from werkzeug.utils import redirect
# custom modules
import utils, views
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'

def logout_page():
    if session is not None:
        session.clear()
    
    return redirect("/")

def main_page():
#    if session.get("loggedin") :
#        return render_template("index.html", columns=["Username", "Link"])
#    else: 
        return redirect("/first")


app.add_url_rule("/", view_func=main_page, methods=["GET", "POST"])
app.add_url_rule("/register", view_func=views.register_page, methods=["GET", "POST"])
app.add_url_rule("/login_admin", view_func=views.login_admin_page, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=logout_page)
app.add_url_rule("/first", view_func=views.first_page)
app.add_url_rule("/admin", view_func=views.admin_page)
app.add_url_rule("/list-users", view_func=views.list_users_page, methods=["GET", "POST"])
app.add_url_rule("/list-places", view_func=views.list_places_page, methods=["GET", "POST"])
app.add_url_rule("/create-users", view_func=views.create_users_page, methods=["GET", "POST"])
app.add_url_rule("/create-places", view_func=views.create_places_page, methods=["GET", "POST"])
app.add_url_rule("/edit-users", view_func=views.edit_users_page, methods=["GET", "POST"])
app.add_url_rule("/edit-places", view_func=views.edit_places_page, methods=["GET", "POST"])
app.add_url_rule("/delete-users", view_func=views.delete_users_page, methods=["GET", "POST"])
app.add_url_rule("/delete-places", view_func=views.delete_places_page, methods=["GET", "POST"])

if __name__ == "__main__":

    app.run(host=config.localhost_ip,port=config.WEB_PORT, debug=True)    
