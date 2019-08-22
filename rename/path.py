from rename import config
import os


def get_directory():
    path = config.get('dir')

    if path:
        while True:
            print('\nEnter (Y/N)')
            directory = input(f'Is your directory: {path}\n> ').lower()

            if directory == 'y':
                break
            elif directory == 'n':
                path = set_directory()
                break
    else:
        path = set_directory()

        config.set('dir', path)
        config.update()

    return path


def set_directory():
    while True:
        directory = input('\nEnter directory:\n> ')

        if os.path.isdir(directory):
            return directory
        else:
            print(f'{directory} is not a directory.')

