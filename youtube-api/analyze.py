import json
import os

REPORTS_DIR = 'out'


def list_playlists(j):
    print('Playlists:', len(j))
    for p in j:
        print(' {}  --  {}'.format(p['snippet']['title'], p['id']))


if __name__ == '__main__':
    if not os.path.exists(REPORTS_DIR):
        raise Exception(f'{REPORTS_DIR} folder not found')
    files = os.listdir(REPORTS_DIR)
    files = [os.path.join(REPORTS_DIR, x)
             for x in files if os.path.splitext(x)[1] == '.json']
    files = sorted(files, key=os.path.getmtime)
    print(files)
    j = None
    with open(files[-2]) as f:
        j = json.load(f)
    print('Loaded')
    list_playlists(j)