from flask import render_template, request, session, flash, send_file
import psycopg2 as dbapi
from werkzeug.utils import redirect
import os
import pandas as pd 
from datetime import datetime

# custom modules
import utils
import config

def register_page():
    conn = None
    try:
        conn = dbapi.connect(config.DSN)
        cur = conn.cursor()
        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            password_conf = request.form["password_conf"]

            if (
                not username
                or not email
                or not password
            ):
                flash("Please fill in all necessary information")
                return render_template("register.html")
            if len(password) < 6:
                flash("Password length should be at least 6")
                return render_template("register.html")
            if password != password_conf:
                flash("Password matching failed")
                return render_template("register.html")

            st = f"SELECT * FROM users WHERE email='{email}'"
            cur.execute(st)
            fetchedUser = cur.fetchone()
            st = f"SELECT * FROM admin WHERE email='{email}'"
            cur.execute(st)
            fetchedAdmin = cur.fetchone()
            if not ((fetchedAdmin is None) and (fetchedUser is None)):
                flash("There is already an existing account with this email")
                return render_template("register.html")

            cur.execute(
                "INSERT INTO users (username, email, \
                            password)\
                            VALUES (%s, %s, %s);",
                (username, email, password),
            )

            flash("Successfully registered")

            return redirect("/login")
        else:
            return render_template("register.html")
    except dbapi.errors.UniqueViolation:
        flash("You are already registered.")
        return render_template("register.html")
    except os.error:
        utils.err_handler(os.error)
        return "Something happened"
    finally:
        cur.close()
        conn.commit()
        conn.close()

def login_page():
    conn = dbapi.connect(config.DSN)
    try:
        cur = conn.cursor()
        if request.method == "POST":
            if "id" in session.keys():
                flash("You are already logged in")
                return render_template("login.html")
            
            email = request.form["email"]
            password = request.form["password"]

            # conn.commit() 
            query = f"SELECT email FROM users WHERE email='{email}'"
            print(query)
            cur.execute(query) 
            fetchedUser = cur.fetchone()

            query = f"SELECT email FROM admin WHERE email='{email}'"
            cur.execute(query) 
            fetchedAdmin = cur.fetchone() 

            if (fetchedAdmin is None) and (fetchedUser is None):
                flash("Invalid email")
                return render_template("login.html")
            
            if fetchedAdmin == None and fetchedUser != None:
                query = f"SELECT id, email, password, username FROM users WHERE email='{email}' and password='{password}'"
                cur.execute(query) 
            else:
                query = f"SELECT id, email, password, username FROM admin WHERE email='{email}' and password='{password}'"
                cur.execute(query) 

            fetched = cur.fetchone()
            if fetched is not None:
                id, email, password_t, username = fetched
                print(query)
                if password_t != password:
                    flash("Invalid Password")
                    return render_template("login.html")

                session["loggedin"] = True
                session["id"] = id
                session["email"] = email
                session["username"] = username
                session["isadmin"] = False if fetchedAdmin == None else True
            
            conn.commit()
            conn.close()
            return redirect("/")
        else:
            return render_template("login.html")
    except dbapi.errors.UniqueViolation:
        flash("You are already logged in")
        return render_template("login.html")
    except os.error:
        flash("Something happened")
        return render_template("login.html")
    

def access_denied():
    return render_template("access-denied.html")
