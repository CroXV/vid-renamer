from rename.config import Config
from rename.regex import regex_name
import os


def folder_crawler(directory):
    name = Config('name')
    current_file = Config('filename')
    current_folder = Config('foldername').save_value(directory)

    # loop through all folders and files in directory
    for foldername, subfolders, files in os.walk(directory):
        # save foldername to config.json
        current_folder.save_value(foldername)
        for file in files:
            # save file name to config.json
            current_file.save_value(file)

            # extract new name from file
            new_name = regex_name(file)
        # delete name key from config.json
        del name.load_value

        for subfolder in subfolders:
            # save sub folder name to config.json
            foldername = os.path.join(foldername, subfolder)
            current_folder.save_value(foldername)