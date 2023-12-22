class User:
    def __init__(self, user_id=None, username=None, user_email=None, user_password=None, user_type=None) -> None:
        self.user_id = user_id
        self.user_name = username
        self.email = user_email
        self.user_type = user_type

    def to_json(self):
        return {key: value for key, value in vars(self).items() if value is not None}