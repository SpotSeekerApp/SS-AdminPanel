class Place:
    def __init__(self, place_name=None, main_category=None, tags=None, link=None) -> None:
        self.place_name = place_name
        self.main_category = main_category
        self.tags = tags
        self.link = link

    def to_json(self):
        return {key: value for key, value in vars(self).items() if value is not None}