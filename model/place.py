class Place:
    def __init__(self, place_name=None, main_category=None, tags=None, link=None) -> None:
        place_name = place_name
        main_category = main_category
        tags = tags
        link = link

    def to_json(self):
        return {key: value for key, value in vars(self).items() if value is not None}