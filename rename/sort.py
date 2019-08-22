from rename import db
from rename import config
import string
import os
import re


def get_name():
    path = db.get('foldername')

    # load name, make new name if name is None
    name = config.get('name')
    if name is None:
        name = input(
            f'\nEnter show name for all episodes in: {path}\n> ')
        config.set('name', name)

    # if name is not all capital, capitalize all first letters.
    if not name.isupper():
        name = string.capwords(name)

    return name


def sort_movie_name(movie):
    name = re.split(r'[-._\s]+', movie)
    name = ' '.join([x.capitalize() for x in name if x])

    return name


def sort_series(series):
    season = re.compile(r's(\d?\d)', re.I).search(series).group(1).zfill(2)
    episode = re.compile(r'e(\d?\d)', re.I).search(series).group(1).zfill(2)

    return f'S{season}E{episode}'


def sort_episode(episode):
    folder = db.get('foldername')

    # check for all episode numbers in files.
    ep = re.compile(r'ep(isode)?[-.(_\s]+?(\d+)', re.I)
    episodes = [int(ep.search(num).group(2)) for num in os.listdir(folder)
                if os.path.isfile(num) and ep.search(num)]
    episodes.sort()

    # use the length of the last episode number as a reference
    # to add zeroes to the front of the episode number.
    if episodes:
        last_num = len(str(episodes[-1]))
        return f'Episode {episode.zfill(last_num)}'
    else:
        return f'Episode {episode}'
