from flask_login import UserMixin
from config import API_URL
import requests
from web_api_admin import Admin, OtherUsers

class User(UserMixin):
    def __init__(self, user_id=None, username=None, user_email=None, user_password=None, user_type=None) -> None:
        self.id = user_id
        self.user_id = user_id
        self.user_name = username
        self.email = user_email
        self.user_type = user_type
        self.user_password = user_password

    def to_json(self):
        return {key: value for key, value in vars(self).items() if value is not None and key != "id"}

    @classmethod
    def add_user_to_db(cls, email, password, username, user_type):
        try:
            user = Admin.add_user(email, password)
            user_json = OtherUsers.sign_in(email, password)
            OtherUsers.send_verification(user_json["idToken"])

            user_data = cls(user_id=user.uid, username=username, user_email=email, user_type=user_type).to_json()
            response = requests.post(f'{API_URL}/AddUser', json=user_data) #TODO: add url
            status = response.json()['StatusCode']
            return user, response
        except:
            raise "Error adding user"
    
    @classmethod
    def sign_in_to_app(cls, email, password, user_type):
        try:
            user = OtherUsers.sign_in(email, password)
            print(user)
            response = requests.get(f'{API_URL}/GetUserInfo?user_id={user["localId"]}')
            res_user_type = response.json()["Data"]["user_type"]
            if res_user_type != user_type:
                raise "Not a place owner!"
            
            user_json = OtherUsers.sign_in(email, password)
            is_verified = OtherUsers.is_verified(user_json["idToken"])
            if is_verified == False:
                raise Exception("Email is not verified!")

            return user,response
        except:
            raise Exception("Sign in error!")

        
    def get_user_from_db(self, user_id):
        response = requests.get(f"{API_URL}GetUserInfo?user_id={user_id}").json()["Data"]
        return User(user_id=user_id, username=response["user_name"], user_email=response["email"], user_type=response["user_type"])