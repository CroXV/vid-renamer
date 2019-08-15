#! python3
# Renames all movies, series, and anime to a much more readable name

import os
import sys
import string
import re
import json
import time


class Path:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # test_dir = f'{script_dir}\\tests'
    json_path = f'{script_dir}\\save\\path.json'
    json_name = f'{script_dir}\\save\\name.json'

    skip_folder = ['Rekt (2012)', '- Animated Series']
    skip_ext = ['.db', '.ini']
    del_ext = ['.jpeg', '.jpg', '.txt', '.nfo', '.info', '.html', '.dat']

    def stored_path(self):
        try:
            with open(self.json_path) as json_file:
                dir_path = json.load(json_file)
            while True:
                user = input(f'Is [{dir_path}] the correct directory?' +
                             '(Enter (Y/N))\n> ').lower()
                if user == 'y':
                    return dir_path
                if user == 'n':
                    self.delete_stored_path()
                    return self.stored_path()
        except FileNotFoundError:
            print('(Press Q to exit.)\nEnter Directory Path:')
            dir_path = input('> ')
            if dir_path.lower() == 'q':
                return dir_path
            with open(self.json_path, 'w') as json_file:
                json.dump(dir_path, json_file)
            return dir_path

    def stored_name(self, file):
        try:
            with open(self.json_name) as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            print('\n(Press Q to exit.)')
            name = input(f'Enter a name for {file} from ' +
                         f'{os.getcwd()}:\n{os.listdir(".")[0:5]}\n> ')
            if name.lower == 'q':
                return 'q'
            with open(self.json_name, 'w') as json_file:
                json.dump(name, json_file)
            return name

    def delete_stored_path(self):
        try:
            os.remove(self.json_path)
        except FileNotFoundError:
            pass

    def delete_stored_name(self):
        try:
            os.remove(self.json_name)
        except FileNotFoundError:
            pass

    @staticmethod
    def check_dir():
        files = [x for x in os.listdir('.') if os.path.isfile(x)]
        folders = [x for x in os.listdir('.') if os.path.isdir(x)]

        return files, folders


class Rename(Path):

    def __init__(self):
        start_time = time.time()
        self.set_dir()
        print(f'--- Took {round(time.time() - start_time, 5)}' +
              's seconds to finish ---')

    def set_dir(self):
        # dir_path = self.test_dir
        dir_path = self.stored_path()
        if os.path.isdir(dir_path):
            os.chdir(dir_path)
            self.crawl_dir()
        elif dir_path == 'q':
            return

    def crawl_dir(self):
        files, folders = self.check_dir()
        self.crawl_files(files)
        self.crawl_folders(folders)

    def crawl_files(self, files):
        for file in files:
            if self.check_ext(file) == 'skip':
                continue
            elif self.regex_file(file) == 'q':
                sys.exit()
        self.delete_stored_name()

    def crawl_folders(self, folders):
        for folder in folders:
            if folder in self.skip_folder:
                continue
            new_folder = self.parse_folder_name(folder)
            try:
                os.chdir(folder)
            except FileNotFoundError:
                os.chdir(new_folder)
            self.crawl_dir()
            os.chdir('..')
            print()

    def check_ext(self, file):
        ext = os.path.splitext(file)[1].lower()
        if ext in self.skip_ext:
            return 'skip'
        elif ext in self.del_ext:
            try:
                os.remove(file)
            except PermissionError:
                pass
            return 'skip'

    def regex_file(self, file):
        file_name = os.path.splitext(file)[0]
        digits = re.compile(r'^\d+$').search(file_name)
        movie = re.compile(r'(.*?)[-.(_\s]?([12]\d{3})').search(file_name)
        anime = re.compile(r'ep(isode)?[-.(_\s]+?(\d+)', re.I).search(file_name)
        series = re.compile(r'''
            ((\d?\d)[-.\s](\d?\d)[-\s]+(.*))|
            (([se]\d?\d[-.(_\s]?[se]\d?\d)[-.\s]*(.*?)[-.(\s]*(720|1080)p)|    
            ([se]\d?\d[-.(_\s]?[se]\d?\d)
            ''', re.I | re.VERBOSE).search(file_name)

        if anime:
            return self.parse_episode_name(file, anime.group(2))
        elif series:
            return self.parse_series_name(file, series)
        elif movie:
            return self.parse_movie_name(file, (movie.group(1), movie.group(2)))
        elif digits:
            return self.parse_episode_name(file, digits.group())

    @staticmethod
    def sort_series(ep_num):
        season = re.compile(r's(\d?\d)', re.I).search(ep_num).group(1).zfill(2)
        episode = re.compile(r'e(\d?\d)', re.I).search(ep_num).group(1).zfill(2)

        return 'S{}E{}'.format(season, episode)

    @staticmethod
    def sort_episode(ep_num):
        num = re.compile(r'ep(isode)?[-.(_\s]+?(\d+)', re.I)
        num_lst = [int(num.search(x).group(2)) for x in os.listdir('.') if os.path.isfile(x)]
        num_lst.sort()
        last_num = len(str(num_lst[-1]))
        return f'Episode {ep_num.zfill(last_num)}'

    def parse_series_name(self, file, series):
        ext = os.path.splitext(file)[1]
        name = self.stored_name(file)
        new_name = None
        if name.lower() == 'q':
            return 'q'
        elif not(name.isupper()):
            string.capwords(name)

        if series.group(1):
            episode = f'S{series.group(2)}E{series.group(3)}'
            desc = string.capwords(series.group(4))
            new_name = f'{name} {episode} - {desc}{ext}'
        elif series.group(5):
            episode = self.sort_series(series.group(6))
            desc = string.capwords(series.group(7))
            new_name = f'{name} {episode} - {desc}{ext}'
        elif series.group(9):
            episode = self.sort_series(series.group(9))
            new_name = f'{name} {episode}{ext}'

        self.renamer(file, new_name)

    def parse_episode_name(self, file, ep_num):
        # Get or set a name for all files in folder.
        ext = os.path.splitext(file)[1]
        ep_num = self.sort_episode(ep_num)
        name = self.stored_name(file)
        # Exit out of file iteration
        if name.lower() == 'q':
            return 'q'
        elif not(name.isupper()):
            name = string.capwords(name)

        new_name = f'{name} {ep_num}{ext}'
        self.renamer(file, new_name, ep_num)

    def parse_movie_name(self, file, groups):
        name, year = groups
        ext = os.path.splitext(file)[1]

        movie = re.split(r'[-._\s]+', name)
        movie = ' '.join([x.capitalize() for x in movie if x])

        new_name = f'{movie} ({year}){ext}'
        self.renamer(file, new_name)

    def parse_folder_name(self, folder):
        movie_folder = re.compile(r'(.*?)[-.(_\s]?([12]\d{3})').search(folder)
        if movie_folder:
            year = movie_folder.group(2)
            movie_folder = re.split(r'[-._\s]+', movie_folder.group(1))
            movie_folder = ' '.join([x.capitalize() for x in movie_folder if x])

            print('\n(Folder)')
            new_folder = f'{movie_folder} ({year})'
            self.renamer(folder, new_folder)
            return new_folder

    def renamer(self, file, new_name, ep_num=None):
        print(f'{file} : {new_name}', end='')
        if file != new_name:
            try:
                os.rename(file, new_name)
                print(' - [done]')
            except OSError:
                print(' - [not done]')
                print('Invalid Characters entered.')
                self.delete_stored_name()
                self.parse_episode_name(file, ep_num)
        else:
            print(' - [skip]')


Rename()
