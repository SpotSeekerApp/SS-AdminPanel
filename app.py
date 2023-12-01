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
    if session.get("loggedin") :
        return render_template("index.html", columns=["Username", "Link"])
    else: 
        return redirect("/login")


app.add_url_rule("/", view_func=main_page, methods=["GET", "POST"])
app.add_url_rule("/register", view_func=views.register_page, methods=["GET", "POST"])
app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=logout_page)

if __name__ == "__main__":

    app.run(host=config.localhost_ip,port=config.WEB_PORT, debug=True)    
