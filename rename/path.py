from rename import config
import os


def get_directory():
    path = config.get('dir')

    if path:
        while True:
            directory = input(f'Is your directory: {path}? (Y/N)').lower()

            if directory == 'n':
                path = set_directory()
            if directory == 'y':
                break
    else:
        path = set_directory()
        config.set('dir', path)

        return path


def set_directory():
    while True:
        directory = input('\nEnter directory:\n> ')

        if os.path.isdir(directory):
            return directory
        else:
            print(f'{directory} is not a directory.')

