'''
Script that obtains tweets of a specific account.
Examples:
https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/User-Lookup/get_users_with_user_context.py
https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/User-Tweet-Timeline/user_tweets.py
API playground:
https://oauth-playground.glitch.me/
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
def parse_tweets(tweets_json):
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
    html_item = '''
<h2>{date}</h2>
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
    attachments_only = True
    for media in media_list:
        if media['type'] == 'photo':
            media_photos[media['media_key']] = media['url']
        elif media['type'] == 'video':
            # TODO: use media['variants'] which looks like this:
            #  "{'bit_rate': 950000, 'content_type': 'video/mp4', 'url': 'https://video.twimg.com/ext_tw_video/1556488702926508032/pu/vid/480x614/Sm38KXv0hYqCKaEv.mp4?tag=12'}"
            media_videos[media['media_key']] = media['preview_image_url']
    for tweet in tweets_json['data']:
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
                logger.warning(f'Unknown attachment in tweet {tweet}')
            if img_url:
                html_extra.append(html_img.format(url=img_url))
        html_tweet = html_item.format(
            date=created, text=text, extra=''.join(html_extra))
        html_result.append(html_tweet)
    html_result.append(html_suffix)
    with open('result.html', 'w') as f:
        f.write(''.join(html_result))


def main():
    username = 'Niseworks'
    uid = get_user_id(username)
    logger.debug(f'{username}: {uid}')
    tweets = get_tweets(uid, max_results=100)
    parse_tweets(tweets)


if __name__ == "__main__":
    main()
