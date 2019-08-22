from rename.settings.app_descriptor import EmptyStringError
import rename.parser as parser
import re
import os


def regex_name(name):
    split = os.path.splitext(name)
    name, ext = split

    anime = re.compile(r'ep(isode)?[-.(_\s]+?(\d+)', re.I).search(name)
    digits = re.compile(r'^\d+$').search(name)
    series = re.compile(r'([se]\d?\d[-.(_\s]?[se]\d?\d)', re.I).search(name)
    movie = re.compile(
        r'(.*?)[-.(_\s](?!1[0-7]\d{2}|\d{4}p)([12]\d{3})').search(name)

    # parse name and return
    try:
        if anime:
            return f'{parser.parse_episode(anime.group(2))}{ext}'
        elif digits:
            return f'{parser.parse_episode(digits.group())}{ext}'
        elif series:
            return f'{parser.parse_series(series.group())}{ext}'
        elif movie:
            return f'{parser.parse_movie(movie.group(1), movie.group(2))}{ext}'
        else:
            return f'{name}{ext}'
    except (TypeError, EmptyStringError):
        return f'{name}{ext}'
