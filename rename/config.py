import json
import logging
# logging.basicConfig(filename='config.log', level=logging.DEBUG,
#                     format='%(asctime)s: %(levelname)s: %(message)s')


class Config:
    # TODO: raise error if value is equal to Q
    def __init__(self, key, value=None):
        self.key = key
        self.value = value

        self.file = 'config.json'
        self.data = self.load_file()

    def load_file(self):
        # tries to load json file and return it.
        # if json file does not exist,
        # it makes a new json file and returns an empty dictionary.
        try:
            data = {}
            with open(self.file) as file:
                data = json.load(file)
        except FileNotFoundError:
            logging.INFO('Creating new json file.')
            with open(self.file, 'w') as file:
                json.dump(data, file)
        finally:
            return data

    def load_value(self):
        try:
            return self.data[self.key]
        except KeyError:
            logging.INFO('Key not found.')

    def save_value(self):
        # set value in loaded data, and update json file with new data.
        self.data[self.key] = self.value
        with open(self.file, 'w') as file:
            json.dump(self.data, file)

        return self.value

    def del_key(self):
        # remove key from dictionary
        self.data.pop(self.key, None)

        with open(self.file, 'w') as file:
            json.dump(self.data, file)
