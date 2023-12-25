
from model.user import User
import requests 
from config import API_URL

user_data = User(user_id="FCmVefFu4PbCGknUXDEkga5uiu72").to_json()
print("user_data", user_data)
response = requests.post(f'{API_URL}/RemoveUser', json=user_data) #TODO: add url
status = response.json()['StatusCode']
response = requests.get(f'{API_URL}/GetAllUsers')

# if status == HTTPStatus.OK:
#     flash("User deleted successfully", "success")
# elif status == HTTPStatus.NOT_ACCEPTABLE:
#     flash({"error": "Same email"}, HTTPStatus.NOT_ACCEPTABLE)
# else:
#     flash({"error": "Failed to remove user"}, HTTPStatus.INTERNAL_SERVER_ERROR)
