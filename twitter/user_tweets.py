'''
Script that obtains tweets of a specific account.
Examples:
https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/User-Lookup/get_users_with_user_context.py
https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/User-Tweet-Timeline/user_tweets.py
API playground:
https://oauth-playground.glitch.me/
https://developer.twitter.com/apitools/downloader
'''

import requests
import os
import json
import logging

DEBUG_THIS = 1
logging.basicConfig(level=(logging.DEBUG if DEBUG_THIS else logging.INFO))
logger = logging.getLogger('user_tweets')

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def check_response(response):
    if response.status_code != 200:
        raise RuntimeError(
            f'Response error: {response.status_code} {response.text}')


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by"
    params = {'usernames': username}
    response = requests.request("GET", url, params=params, auth=bearer_oauth)
    check_response(response)
    jresp = response.json()
    return jresp['data'][0]['id']


def get_tweets(uid, max_results=None, pagination_token=None, start_time=None, end_time=None):
    """
    max_results = [5,10] (default: 10)
    JSON response format:
    {
        data: [{attachements: {media_keys: [str, ...]}, created_at: str, id: str, text: str}, ...],
        includes: {media: [{media_key: str, type: str, url: str}, ...]},
        meta: {newest_id: str, next_token: str, , oldest_id: str, result_count: int}
    }
    next_token is for pagination.
    """
    url = f"https://api.twitter.com/2/users/{uid}/tweets"
    params = {'max_results': max_results, 'pagination_token': pagination_token, 'tweet.fields': 'created_at', 'expansions': 'attachments.media_keys',
              'media.fields': 'type,url,preview_image_url,variants', 'start_time': start_time, 'end_time': end_time}
    response = requests.request("GET", url, params=params, auth=bearer_oauth)
    check_response(response)
    jresp = response.json()
    return jresp


# TODO: split this func
# TODO: support pagination of output
def parse_tweets(tweets_json, attachments_only=False):
    meta = tweets_json.get('meta')
    logger.debug(f'meta: {meta}')
    html_prefix = '''
<!DOCTYPE html>
<html>
<head>
</head>
<body>
    '''
    html_suffix = '''
</body>
</html>
    '''
    # TODO: replace id by a link:
    #  https://twitter.com/Niseworks/status/594261874822279168
    html_item = '''
<h2>{title}</h2>
<p><b>id:</b>{id}</p>
<p>{text}</p>
{extra}
<hr/>
    '''
    html_img = '<img src="{url}">'
    html_result = []
    html_result.append(html_prefix)
    media_list = tweets_json['includes']['media']
    media_photos = {}
    media_videos = {}
    for media in media_list:
        if media['type'] == 'photo':
            media_photos[media['media_key']] = media['url']
        elif media['type'] == 'video':
            # TODO: use media['variants'] which looks like this:
            #  "{'bit_rate': 950000, 'content_type': 'video/mp4', 'url': 'https://video.twimg.com/ext_tw_video/1556488702926508032/pu/vid/480x614/Sm38KXv0hYqCKaEv.mp4?tag=12'}"
            # https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/media
            media_videos[media['media_key']] = media['preview_image_url']
    for i, tweet in enumerate(tweets_json['data']):
        # TODO: substitute t.co link?
        attachement_list = tweet.get('attachments')
        if attachement_list:
            attachement_list = attachement_list['media_keys']
        elif attachments_only:
            continue
        else:
            attachement_list = []
        created = tweet['created_at']
        text = tweet['text']
        html_extra = []
        for attachement in attachement_list:
            img_url = media_photos.get(attachement)
            if img_url is None:
                img_url = media_videos.get(attachement)
                html_extra.append('<h3>Video preview</h3>')
            if img_url is None:
                # TODO: support more types
                # Unknown attachment in tweet {'attachments': {'media_keys': ['16_1149492687088676865']}, 'created_at': '2019-07-12T01:37:44.000Z', 'text': 'I forgot to upload this gif without sound. Hope you guys like it. Second part coming next week!\n#niseworks #nisego https://t.co/tSm5W7hV9L', 'id': '1149493010691813376'}
                logger.warning(f'Unknown attachment in tweet {tweet}')
            if img_url:
                html_extra.append(html_img.format(url=img_url))
        html_tweet = html_item.format(
            title=f'{i+1}. {created}', text=text, extra=''.join(html_extra), id=tweet['id'])
        html_result.append(html_tweet)
    html_result.append(html_suffix)
    with open('result.html', 'w') as f:
        f.write(''.join(html_result))


def merge_json(a, b):
    if not a and b:
        return b
    elif not b:
        return a
    a['data'].extend(b['data'])
    a['includes']['media'].extend(b['includes']['media'])
    return a


def get_tweets_iter(uid, max_results=None):
    result = {}
    pagination_token = None
    try:
        while True:
            tweets = get_tweets(uid, max_results=100,
                                pagination_token=pagination_token)
            result = merge_json(result, tweets)
            pagination_token = tweets['meta'].get('next_token')
            if not pagination_token:
                logger.debug(f'No pagination token, stop. {tweets["meta"]}')
                break
    except BaseException as err:
        logger.exception(err)
    return result


def main():
    username = 'Niseworks'
    uid = get_user_id(username)
    logger.debug(f'{username}: {uid}')
    tweets = get_tweets_iter(uid)
    # tweets = get_tweets(uid, end_time='2016-03-30T22:11:18.000Z', max_results=100)
    # oldest attachment: 2016-02-10T18:04:32.000Z https://t.co/8mSy5gFswd
    # oldest tweet http://t.co/hSPfs5deDf
    parse_tweets(tweets)


if __name__ == "__main__":
    main()
