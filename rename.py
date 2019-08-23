from rename.database import NoNameError
from rename.walk import walk_dir
from rename.path import get_path
from rename import db
import os
import sys


def renamer():
    print('\nPress (Y/N) to continue...')
    while True:
        confirm = input('> ').lower()

        if confirm == 'q' or confirm == 'n':
            print('\nClosing script...')
            sys.exit()
        elif confirm == 'y':
            for k, v in db.database.items():
                os.rename(k, v)
            print('\nDone')
            break


def main():
    print('(Press Q to exit script.)')
    directory = get_path()
    walk_dir(directory)

    print('\nRenaming:')
    try:
        db.print_database()
        renamer()
    except NoNameError as err:
        print(err)


if __name__ == '__main__':
    main()
