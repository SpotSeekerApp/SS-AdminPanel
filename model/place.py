class Place:
    def __init__(self, place_id=None, place_name=None, main_category=None, tags=None, link=None, user_id=None) -> None:
        self.place_name = place_name
        self.main_category = main_category
        self.tags = tags
        self.link = link
        self.user_id = user_id
        self.place_id = place_id

    def to_json(self):
        return {key: value for key, value in vars(self).items() if value is not None}