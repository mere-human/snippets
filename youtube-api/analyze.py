import json
import os

REPORTS_DIR = 'out'


def list_playlists(root_json):
    print('Playlists:', len(root_json))
    for p in root_json:
        print('  {} - {}'.format(p['snippet']['title'], p['id']))


def list_videos(pl_json):
    items = pl_json['items']
    print('Videos:', len(items))
    for x in items:
        print('  {} {}'.format(x['snippet']['position'], x['snippet']['title']))


if __name__ == '__main__':
    if not os.path.exists(REPORTS_DIR):
        raise Exception(f'{REPORTS_DIR} folder not found')
    files = os.listdir(REPORTS_DIR)
    files = [os.path.join(REPORTS_DIR, x)
             for x in files if os.path.splitext(x)[1] == '.json']
    files = sorted(files, key=os.path.getmtime)
    print(files)
    root = None
    with open(files[-2]) as f:
        root = json.load(f)
    print('Loaded')
    list_playlists(root)
    list_videos(root[0])
