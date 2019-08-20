from json.decoder import JSONDecodeError
import json


class Config:
    def __init__(self, key, value):
        self.key = key
        self.value = value

        self.save_file = 'config.json'
        self.data = {}

    def load_json_value(self):
        try:
            with open(self.save_file) as file:
                self.data = json.load(file)
                return self.data[self.key]
        except KeyError:
            pass

    def save_json_value(self):
        try:
            with open(self.save_file) as file:
                self.data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            pass
        finally:
            self.data[self.key] = self.value
            with open('config.json', 'w') as file:
                json.dump(self.data, file)

            return self.data[self.key]

    def del_json_key(self):
        with open(self.save_file) as file:
            self.data = json.load(file)
            self.data.pop(self.key, None)

        with open(self.save_file, 'w') as file:
            json.dump(self.data, file)
