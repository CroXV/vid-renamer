from rename.walk import walk_dir
from rename.path import get_directory


def renamer():
    print('(Enter Q to exit script.)')
    directory = get_directory()
    walk_dir(directory)


if __name__ == '__main__':
    renamer()
