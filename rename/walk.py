from rename import db
from rename import config
from rename.regex import regex_name
from rename.settings.app_descriptor import EmptyStringError
import os


def walk_dir(directory):
    # go through all files in folder and store them in database with a new name
    for foldername, subfolders, files in os.walk(directory):
        # save current folder name to database
        db.set('foldername', foldername)

        try:
            for file in files:
                name = regex_name(file)
                filename = os.path.join(foldername, file)
                new_filename = os.path.join(foldername, name)

                db.add(filename, new_filename)
        except (TypeError, EmptyStringError):
            pass
        finally:
            config.del_value('name')

        for subfolder in subfolders:
            name = regex_name(subfolder)
            subfolder = os.path.join(foldername, subfolder)
            new_subfolder = os.path.join(foldername, name)

            db.set('foldername', subfolder)
            db.add(subfolder, new_subfolder)

    db.update()
    config.update()

