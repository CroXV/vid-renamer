from rename.config import Config
import string
import os
import re


def sort_episode(episode):
    folder = Config('foldername').load_value

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


def sort_name():
    name = Config('name')
    path = Config('foldername').load_value

    # load name, make and save new name in config.json, if name doesn't exist.
    show_name = name.load_value
    if not show_name:
        show_name = input(f'\nEnter a name for all files in {path}:\n> ')
        name.save_value(show_name)
    # if name is not all capital, capitalize all first letters.
    if not show_name.isupper():
        show_name = string.capwords(show_name)

    return show_name


def sort_series(series):
    if series.group(1):
        episode = f'S{series.group(2)}E{series.group(3)}'
        desc = string.capwords(series.group(4))
        return f'{episode} - {desc}'
    elif series.group(5):
        episode = sort_series_episode(series.group(6))
        desc = string.capwords(series.group(7))
        return f'{episode} - {desc}'
    elif series.group(9):
        episode = sort_series_episode(series.group(9))
        return f'{episode}'


def sort_series_episode(series):
    season = re.compile(r's(\d?\d)', re.I).search(series).group(1).zfill(2)
    episode = re.compile(r'e(\d?\d)', re.I).search(series).group(1).zfill(2)

    return f'S{season}E{episode}'
