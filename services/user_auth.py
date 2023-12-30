import json
import http
import requests
import pyrebase
from firebase_admin import auth
from firebase_admin import initialize_app
from firebase_admin import credentials
import config

WEBAPIKEY="AIzaSyAfYvTIs8C1DfruUHgYR0AxhiKtwULVrFw"

def load_cred_from_config():
    cred_dict = {
        "type": config.TYPE,
        "project_id": config.PROJECT_ID,
        "private_key_id": config.PRIVATE_KEY_ID,
        "private_key": config.PRIVATE_KEY.replace('\\n', '\n'),
        "client_email": config.CLIENT_EMAIL,
        "client_id": config.CLIENT_ID,
        "auth_uri": config.AUTH_URI,
        "token_uri": config.TOKEN_URI,
        "auth_provider_x509_cert_url": config.AUTH_PROVIDER_X509_CERT_URL,
        "client_x509_cert_url": config.CLIENT_X509_CERT_URL,
        "universe_domain": config.UNIVERSE_DOMAIN
    }

    return cred_dict

cred = credentials.Certificate(load_cred_from_config())
firebase = initialize_app(credential=cred)


class Admin:
    def add_user(email, password):
        try:
            user = auth.create_user(email=email, password=password, app=firebase)
            print('Sucessfully created new user: {0}'.format(user.uid))
        except Exception as e:
            msg = 'Cannot create new user: {0}'.format(e)
            print(msg)
            return -1, msg

        return 0, user

    def update_user(user_id, email, password):
        try:
            user = auth.update_user(user_id, email=email, password=password, app=firebase)
            print('Sucessfully updated user: {0}'.format(user.uid))
        except Exception as e:
            print('Cannot update the user: {0}'.format(e))    

    def remove_user(user_id):
        auth.delete_user(user_id, app=firebase)
        print('Sucessfully deleted user: {0}'.format(user_id))

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
        
        return response.json()

    def send_reset_password_mail(email):
        body = {
            "requestType": "PASSWORD_RESET",
            "email": email
        }

        response = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={WEBAPIKEY}", data=body)

        if response.status_code != http.HTTPStatus.OK:
            pass
        else:
            pass

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

        return response.json()["users"][0]["emailVerified"]
