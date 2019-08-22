#!/usr/bin/env python3

from rename.app_descriptor import ExitScript
import json


class Config:
    # descriptor to check if exit conditions are met.
    value = ExitScript()

    def __init__(self):
        self.file = 'config.json'
        self.data = self.load()

    def load(self):
        # try to load json file and return it.
        data = {}
        try:
            with open(self.file) as file:
                data = json.load(file)
        except FileNotFoundError:
            pass
        finally:
            return data

    def update(self):
        with open(self.file, 'w') as file:
            json.dump(self.data, file)

    def set(self, key, value):
        # update instance value
        self.value = value
        # set key to value in instance data
        self.data[key] = value

    def get(self, key):
        # try to get value from loaded data if key exists.
        try:
            return self.data[key]
        except KeyError:
            pass

    def del_value(self, key):
        # remove key from dictionary and update json file.
        self.data.pop(key, None)
