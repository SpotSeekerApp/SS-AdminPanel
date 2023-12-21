class User:
    def __init__(self, user_id=None, username=None, user_email=None, user_password=None, user_type=None) -> None:
        user_id = user_id
        username = username
        user_email = user_email
        user_password = user_password
        user_type = user_type

    def to_json(self):
        return {key: value for key, value in vars(self).items() if value is not None}