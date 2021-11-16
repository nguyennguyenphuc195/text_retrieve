import json


class JSONFile:
    """
    Used for train and test data json
    """
    def __init__(self, json_fn):
        self.json_content = json.load(open(json_fn))
        self.name = self.json_content["_name_"]
        self.datetime = self.json_content["_date_time_"]
        self.count = self.json_content["_count_"]
        self.items = self.json_content["items"]


class Law:
    def __init__(self, dict_obj):
        self.law_id = dict_obj["law_id"]
        self.articles = dict_obj["articles"]


class Corpus:
    def __init__(self, json_fn):
        self.json_content = json.load(open(json_fn))
        self.laws = []
        for item in self.json_content:
            self.laws.append(Law(item))
