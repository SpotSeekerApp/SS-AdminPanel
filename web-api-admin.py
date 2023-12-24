import json
import http
import requests
import pyrebase
from firebase_admin import auth
from firebase_admin import initialize_app
from firebase_admin import credentials

WEBAPIKEY="AIzaSyAfYvTIs8C1DfruUHgYR0AxhiKtwULVrFw"

class Admin:
    def add_user(email, password):
        cred = credentials.Certificate("./credential-token.json")

        # Initialize Firebase
        firebase = initialize_app(credential=cred)

        try:
            user = auth.create_user(email=email, password=password, app=firebase)
            print('Sucessfully created new user: {0}'.format(user.uid))
        except Exception as e:
            print('Cannot create new user: {0}'.format(e))    

    def update_user(user_id, email, password):
        cred = credentials.Certificate("./credential-token.json")

        # Initialize Firebase
        firebase = initialize_app(credential=cred)

        try:
            user = auth.update_user(user_id, email=email, password=password, app=firebase)
            print('Sucessfully updated user: {0}'.format(user.uid))
        except Exception as e:
            print('Cannot update the user: {0}'.format(e))    

    def remove_user(user_id):

        cred = credentials.Certificate("./credential-token.json")

        # Initialize Firebase
        firebase = initialize_app(credential=cred)

        auth.delete_user(user_id, app=firebase)

class OtherUsers:
    def sign_in(email, password):
        body = {
            "email": email,
            "password": password
        }

        response = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={WEBAPIKEY}", data=body)

        if response.status_code != http.HTTPStatus.OK:
            try: 
                print("Error", response.json()["error"]["message"])
            except KeyError:
                print("Unknown error")
        else:
            print("Signed in -> user_id:", response.json()["localId"])
        
        return response.json()["idToken"]

    def changePassword(idToken):
        body = {
            "idToken": idToken,
            "password": "asdasfdsfsadf"
        }

        response = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={WEBAPIKEY}", data=body)

        if response.status_code != http.HTTPStatus.OK:
            try: 
                print("Error", response.json()["error"]["message"])
            except KeyError:
                print("Unknown error")
        else:
            print("Password updated -> user_id:", response.json()["localId"])

    def send_verification(idToken):
        body = {
            "requestType": "VERIFY_EMAIL",
            "idToken": idToken
        }

        response = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={WEBAPIKEY}", data=body)

        if response.status_code != http.HTTPStatus.OK:
            try: 
                print("Error", response.json()["error"]["message"])
            except KeyError:
                print("Unknown error")
        else:
            print("Send email -> ", response.json()["email"])

    def is_verified(idToken):
        body = {
            "idToken": idToken
        }

        response = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={WEBAPIKEY}", data=body)

        if response.status_code != http.HTTPStatus.OK:
            try: 
                print("Error", response.json()["error"]["message"])
            except KeyError:
                print("Unknown error")
        else:
            print("isVerified -> ", response.json()["users"][0]["emailVerified"])

    

#Admin.remove_user("CxZz7fGjDGSwaHYbOnXHDxhGnEh1")
#Admin.add_user("mertcanarabaci2001@gmail.com", "asdasd123!")
id_token = OtherUsers.sign_in("mertcanarabaci2001@gmail.com", "asdasd123!")
#print("id_token: ", id_token)
#OtherUsers.is_verified(id_token)
#OtherUsers.send_verification(id_token)
OtherUsers.is_verified(id_token)



