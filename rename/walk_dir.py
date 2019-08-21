from rename.config import Config
from rename.regex import regex_name
import os


def walk_dir(directory):
    # set config keys
    name = Config('name')
    current_file = Config('filename')
    current_folder = Config('foldername').save_value(directory)

    # loop all folders and files in dir while saving paths to config.json
    for foldername, subfolders, files in os.walk(directory):
        current_folder.save_value(foldername)

        for file in files:
            current_file.save_value(file)
            new_name = regex_name(file)
        del name.load_value  # delete name key from config.json

        for subfolder in subfolders:
            # save subfolder name to config.json
            foldername = os.path.join(foldername, subfolder)
            current_folder.save_value(foldername)
