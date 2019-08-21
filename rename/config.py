#!/usr/bin/env python3

from rename.app import ExitScript
import json
import logging
# logging.basicConfig(filename='config.log', level=logging.DEBUG,
#                     format='%(asctime)s: %(levelname)s: %(message)s')


class Config:
    # decorater to check if exit conditions are met.
    value = ExitScript()

    def __init__(self, key):
        self.key = key

        self.file = 'config.json'
        self.data = {}

    def update_data(self):
        # try to load json file and return it.
        # if json file is not found, make a new json file.
        try:
            with open(self.file) as file:
                self.data = json.load(file)
        except FileNotFoundError:
            logging.info('Creating new json file...')
            with open(self.file, 'w') as file:
                json.dump(self.data, file)

    def save_value(self, value):
        # update instance and data values
        self.update_data()
        self.value = value

        # set value in loaded data and update json file with new data.
        self.data[self.key] = value
        with open(self.file, 'w') as file:
            print(self.data)
            json.dump(self.data, file, sort_keys=True, indent=4)

    @property
    def load_value(self):
        # update data value
        self.update_data()
        # try to get value from loaded data if key exists.
        try:
            return self.data[self.key]
        except KeyError:
            logging.info('Key not found.')

    @load_value.deleter
    def load_value(self):
        # update data value
        self.update_data()
        # remove key from dictionary and update json file.
        self.data.pop(self.key, None)
        with open(self.file, 'w') as file:
            json.dump(self.data, file, sort_keys=True, indent=4)
