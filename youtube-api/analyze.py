import json
import os
from dump import DATETIME_FORMAT
from datetime import datetime

REPORTS_DIR = 'out'


def get_snippet_str(item, published=True):
    snippet = item['snippet']
    result = snippet['title']
    if published and 'publishedAt' in snippet:
        result += ' - '
        result += snippet['publishedAt']
    return result


def list_playlists(root_json, show_len=False, show_id=False, show_missing=False):
    print('Playlists:', len(root_json))
    for p in root_json:
        s = p['snippet']['title']
        if show_len:
            s += ' - '
            s += str(len(p['items']))
        if show_id:
            s += ' - '
            s += p['id']
        print(' ', s)
        if show_missing:
            missing_positions = detect_deleted_videos(p)
            if missing_positions:
                print('    Missing videos: {} at {}'.format(len(missing_positions),
                                                            ', '.join(missing_positions).rstrip(',')))


def list_videos(pl_json):
    items = pl_json['items']
    print('Videos:', len(items))
    for x in items:
        print('  {} {}'.format(x['snippet']
                               ['position'], x['snippet']['title']))


def detect_deleted_videos(pl_json):
    result = []
    last_pos = -1
    items = pl_json['items']
    for x in items:
        pos = x['snippet']['position']
        if last_pos + 1 != pos:
            result.append(str(last_pos+1))
        last_pos = pos
    return result


def date_from_file_name(file_name):
    base = os.path.basename(file_name)
    sep = '.'
    parts = base.split(sep)
    if len(parts) == 4:
        base = sep.join(parts[1:3])
        return datetime.strptime(base, DATETIME_FORMAT)
    ctime = os.path.getctime(file_name)
    return datetime.fromtimestamp(ctime)


def diff_playlists(root1, root2, file_name1, file_name2):
    date1 = date_from_file_name(file_name1)
    date2 = date_from_file_name(file_name2)
    print('Diff ({}):'.format(date2-date1))
    if root1 == root2:
        print('Identical')
        return

    # 1. Check playlists
    map1 = dict()
    map2 = dict()
    # Map id to position
    for i, x in enumerate(root1):
        map1[x['id']] = i
    for i, x in enumerate(root2):
        map2[x['id']] = i
    # Check ids
    set1 = set(map1.keys())
    set2 = set(map2.keys())
    if map1.keys() != map2.keys():
        for x in set1.difference(set2):
            print('-', get_snippet_str(root1[map1[x]]))
        for x in set2.difference(set1):
            print('+', get_snippet_str(root2[map2[x]]))

    # 2. Check videos in playlists
    superset = set1.intersection(set2)
    for x in superset:
        # Map video id to position
        items1 = root1[map1[x]]['items']
        map_items1 = dict()
        for i, y in enumerate(items1):
            map_items1[y['snippet']['resourceId']['videoId']] = i

        items2 = root2[map2[x]]['items']
        map_items2 = dict()
        for i, y in enumerate(items2):
            map_items2[y['snippet']['resourceId']['videoId']] = i

        # Check ids
        set_keys1 = set(map_items1.keys())
        set_keys2 = set(map_items2.keys())
        if set_keys1 != set_keys2:
            print('*', root1[map1[x]]['snippet']['title'])
            for y in set_keys1.difference(set_keys2):
                print('  -', get_snippet_str(items1[map_items1[y]]))
            for y in set_keys2.difference(set_keys1):
                print('  +', get_snippet_str(items2[map_items2[y]]))


if __name__ == '__main__':
    if not os.path.exists(REPORTS_DIR):
        raise Exception(f'{REPORTS_DIR} folder not found')
    files = os.listdir(REPORTS_DIR)
    files = [os.path.join(REPORTS_DIR, x)
             for x in files if os.path.splitext(x)[1] == '.json']
    files = sorted(files, key=os.path.getmtime)

    file_name1 = files[-2]
    with open(file_name1) as f:
        root1 = json.load(f)
    print('Loaded', file_name1)

    file_name2 = files[-1]
    with open(file_name2) as f:
        root2 = json.load(f)
    print('Loaded', file_name2)

    list_playlists(root2, show_len=True, show_missing=True)

    diff_playlists(root1, root2, file_name1, file_name2)
