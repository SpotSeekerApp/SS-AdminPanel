from flask_login import LoginManager
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
# custom modules
import config

from controller import main_controller, placeowner_controller, admin_controller, common_controller
from model.user import User
from services.logger import logger

# login manager
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    logger.info(f"Loading user user_id:{user_id}")
    user = User()
    user.get_user_from_db(user_id)
    return user

@login_manager.unauthorized_handler
def unauthorized():
    logger.info("Unauthorized endpoint.")
    return render_template("index.html")

def create_app():
    logger.info(f"Creating Flask app")
    
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY
    # app.config['SESSION_TYPE'] = 'filesystem'


    login_manager.init_app(app)

    app.add_url_rule("/", view_func=main_controller.main_page, methods=["GET", "POST"]) # main page 
    app.add_url_rule("/logout", view_func=main_controller.logout_page,  methods=["GET", "POST"])
    app.add_url_rule("/register", view_func=placeowner_controller.register_page, methods=["GET", "POST"])
    app.add_url_rule("/login-placeowner", view_func=placeowner_controller.login_placeowner_page, methods=["GET", "POST"])
    app.add_url_rule("/reset-password", view_func=placeowner_controller.reset_password_page, methods=["GET", "POST"])

    app.add_url_rule("/list-users", view_func=admin_controller.list_users_page, methods=["GET"])
    app.add_url_rule("/list-places", view_func=common_controller.list_places_page, methods=["GET"])

    app.add_url_rule("/create-users", view_func=admin_controller.create_users_page, methods=["POST"])
    app.add_url_rule("/create-places", view_func=common_controller.create_places_page, methods=["GET", "POST"])

    app.add_url_rule("/delete-users/<string:user_id>", view_func=admin_controller.delete_users_page, methods=["GET", "POST"])
    app.add_url_rule("/delete-places/<string:place_id>", view_func=common_controller.delete_places_page, methods=["GET", "POST"])
    app.add_url_rule("/update-users", view_func=admin_controller.update_users_page, methods=["GET", "POST"])
    app.add_url_rule("/update-places", view_func=common_controller.update_places_page, methods=["GET", "POST"])

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host=config.LOCALHOST_IP, port=config.PORT, debug=True)    

