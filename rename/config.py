#!/usr/bin/env python3

from rename.app import ExitProgram
import json
import logging
# logging.basicConfig(filename='config.log', level=logging.DEBUG,
#                     format='%(asctime)s: %(levelname)s: %(message)s')


class Config:
    # check if exit conditions are met
    value = ExitProgram()

    def __init__(self, key):
        self.key = key

        self.file = 'config.json'
        self.data = self.load_file()

    def load_file(self):
        # try to load json file and return it.
        # if json file does not exist,
        # make a new json file and return an empty dictionary.
        try:
            data = {}
            with open(self.file) as file:
                data = json.load(file)
        except FileNotFoundError:
            logging.info('Creating new json file...')
            with open(self.file, 'w') as file:
                json.dump(data, file)
        finally:
            return data

    def save_value(self, value):
        # update config value
        self.value = value
        # set value in loaded data and update json file with new data.
        self.data[self.key] = value
        with open(self.file, 'w') as file:
            json.dump(self.data, file)
        return value

    @property
    def load_value(self):
        # try to get value from loaded data if key exists.
        try:
            return self.data[self.key]
        except KeyError:
            logging.warning('Key not found.')

    @load_value.deleter
    def load_value(self):
        # remove key from dictionary and update json file.
        self.data.pop(self.key, None)
        with open(self.file, 'w') as file:
            json.dump(self.data, file)
