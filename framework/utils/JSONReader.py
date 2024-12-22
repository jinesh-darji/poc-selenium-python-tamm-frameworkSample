import json


class JSONReader:

    @staticmethod
    def read(file_path):
        with open(file_path) as raw_data:
            return json.loads(raw_data.read())
