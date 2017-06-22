import json


class FeedColumn:
    def __init__(self, type, search_path, path, name, display_name):
        self.type = type
        self.display_name = display_name
        self.name = name
        self.path = path
        self.search_path = search_path

    def __str__(self):
        return json.dumps(self.__dict__)

