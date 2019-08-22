import rename.sort as sort


def parse_episode(episode):
    name = sort.get_name()
    episode = sort.sort_episode(episode)

    return f'{name} {episode}'


def parse_series(series):
    name = sort.get_name()
    series = sort.sort_series(series)

    return f'{name} {series}'


def parse_movie(name, year):
    movie = sort.sort_movie_name(name)

    return f'{movie} ({year})'
