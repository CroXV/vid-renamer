import os, re


def test_dir():
    path = os.path.dirname(os.path.abspath(__file__)) + r'\tests'
    os.chdir(path)


def make():
    test_dir()
    for x in range(1, 101):
        n_path = f'this.is.spartacus.episode.{str(x)}.mp4'
        with open(n_path, "w") as f:
            f.write('')


def remove():
    test_dir()
    for file in os.listdir('.'):
        os.remove(file)

#
# remove()
# make()


le = 'SAO S01E03 The Red-Nosed Reindeer (720p ENG) v2'
le = 'Victorious.S01E04.The.Birthweek.Song.720p.WEB-DL.AAC.H264-SURFER'
rem = re.compile(r'(([se]\d?\d[-.(_\s]?[se]\d?\d)[-.\s]*(.*?)[-.(\s]*(720|1080)p)', re.I).search(le)
print(rem.group(3))