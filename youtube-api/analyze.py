import json
import os

REPORTS_DIR = 'out'


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


if __name__ == '__main__':
    if not os.path.exists(REPORTS_DIR):
        raise Exception(f'{REPORTS_DIR} folder not found')
    files = os.listdir(REPORTS_DIR)
    files = [os.path.join(REPORTS_DIR, x)
             for x in files if os.path.splitext(x)[1] == '.json']
    files = sorted(files, key=os.path.getmtime)
    root = None
    file_name = files[-1]
    with open(file_name) as f:
        root = json.load(f)
    print('Loaded', file_name)
    list_playlists(root, show_len=True, show_missing=True)
