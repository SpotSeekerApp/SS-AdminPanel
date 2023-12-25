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
            return None

        return user

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
        
        return response.json()

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

        return response.json()["users"][0]["emailVerified"]

    

# Admin.remove_user("2uxQLwH1R7YoV8l8flvOIISoe223")
# #Admin.add_user("mertcanarabaci2001@gmail.com", "asdasd123!")
# id_token = OtherUsers.sign_in("gundogdue19@itu.edu.tr", "Leonreino*1")
# print("id_token: ", id_token)
# Admin.remove_user(id_token["localId"])

# user_data = {"user_id":"UFqn0N9m0IPO22JxxKaHlWu3vs03"}
# print("user_data", user_data)
# response = requests.post(f'{"https://database-demo-api-5igkar365a-oa.a.run.app/"}/RemoveUser', json=user_data) #TODO: add url
# # #OtherUsers.is_verified(id_token)
# OtherUsers.send_verification("eyJhbGciOiJSUzI1NiIsImtpZCI6ImxrMDJBdyJ9.eyJpc3MiOiJodHRwczovL2lkZW50aXR5dG9vbGtpdC5nb29nbGUuY29tLyIsImF1ZCI6Im1lcnQtcGVyc29uYWwiLCJpYXQiOjE3MDM1MTQzOTMsImV4cCI6MTcwNDcyMzk5MywidXNlcl9pZCI6ImhTOWpTTFJPdXhTMmxVaDVuY1gxblBNdWVNQzIiLCJlbWFpbCI6Imd1bmRvZ2R1LmVtaXJjYW5Ab3V0bG9vay5jb20iLCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQiLCJ2ZXJpZmllZCI6ZmFsc2V9.nE3dimcEGxnHvl6Uzcb7edhpFK2Zhh54g9dT7q94JM8V-cWXATA6IFMFWRHE2rikiaXjQPs6qhedukv7Rsh4uEt4YQSDSdxEV3hUSLv5VIIQxSgCQB_HJ6iYfiyAyPX1MnwnAmG8CK_IpqJ6muzcMy_6XQ25ZFhta3tMhAm_zYPjFJrqIXKuIKjwmcXK_jd8sxzP1L51MnD9Fk-btI627QnxC9XMRLDSCr0jY6M-kfHD5Rz59ZZSrUD3lpkHMYaUo-URKLTO_2uTVONE1t5KlcmOH-LoKdeJev_hN3Ciq-QFq0eSQXb0xlWESykMv81gJB-8VW_Hgub2hM8_gu1Otw")

# # user_data = {"user_id":"2uxQLwH1R7YoV8l8flvOIISoe223"}
# # print("user_data", user_data)
# # response = requests.post(f'{"https://database-demo-api-5igkar365a-oa.a.run.app/"}/RemoveUser', json=user_data) #TODO: add url


# name = "THEONE"
# email = "gundogdu.emircan@outlook.com"
# password = "Leonreino*1"

# Admin.add_user(email, password)
# user_json = OtherUsers.sign_in(email, password)
# print("id_token: ", user_json)
# Admin.remove_user(user_json["localId"])


# # user = Admin.add_user(email, password)

user_data = {
    "user_name":"THEONE",
    "user_id":"hS9jSLROuxS2lUh5ncX1nPMueMC2",
    "email":"gundogdu.emircan@outlook.com",
    "user_type":"admin" # normal, place_owner, admin 
}

response = requests.post(f'{"https://database-demo-api-5igkar365a-oa.a.run.app/"}/RemoveUser', json={"user_id":"aaMvEJt0zgNjB5FOkfH9WFCO0VO2"})

response = requests.post(f'{"https://database-demo-api-5igkar365a-oa.a.run.app/"}/AddUser', json=user_data)
print(response)