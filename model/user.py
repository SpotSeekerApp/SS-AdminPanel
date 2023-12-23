from flask_login import UserMixin
from config import API_URL
import requests

class User(UserMixin):
    def __init__(self, user_id=None, username=None, user_email=None, user_password=None, user_type=None) -> None:
        self.id = user_id
        self.user_id = user_id
        self.user_name = username
        self.email = user_email
        self.user_type = user_type

    def to_json(self):
        return {key: value for key, value in vars(self).items() if value is not None and key != "id"}
    
    def get_user_from_db(self, user_id):
        response = requests.get(f"{API_URL}GetUserInfo?user_id={user_id}").json()["Data"]
        return User(user_id=user_id, username=response["user_name"], user_email=response["email"], user_type=response["user_type"])