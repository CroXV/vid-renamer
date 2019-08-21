import rename.parser as parser
import re
import os


def regex_name(name):
    split = os.path.splitext(name)
    name, ext = split

    digits = re.compile(r'^\d+$').search(name)
    movie = re.compile(r'(.*?)[-.(_\s]?([12]\d{3})').search(name)
    anime = re.compile(r'ep(isode)?[-.(_\s]+?(\d+)', re.I).search(name)
    series = re.compile(r'''
                # group 1, 5, 9: (respectively)
                # 1: with text, 5: without notation, 9: with notation
                (([se]\d?\d[-.(_\s]?[se]\d?\d)[-.\s]*(.*?)[-.(\s]*(720|1080)p)|
                ((\d?\d)[-.\s](\d?\d)[-\s]+(.*))|
                ([se]\d?\d[-.(_\s]?[se]\d?\d)
                ''', re.I | re.VERBOSE).search(name)

    if anime:
        return f'{parser.parse_episode(anime.group(2))}{ext}'
    elif digits:
        return f'{parser.parse_episode(digits.group())}{ext}'
    elif series:
        return f'{parser.parse_series(series)}{ext}'
    elif movie:
        movie = (movie.group(1), movie.group(2))
        return f'{parser.parse_movie(name, movie)}{ext}'


