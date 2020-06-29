#!/usr/bin/python3

# Retrieve the authenticated user's uploaded videos.
# Sample usage:
# python my_uploads.py

import argparse
import os
import re
import json
import sys
import pickle
import os.path

from datetime import datetime
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = 'client_secret.json'

# This OAuth 2.0 access scope allows for read-only access to the authenticated
# user's account, but not other types of account access.
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


# Authorize the request and store authorization credentials.
def get_authenticated_service():
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
      creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
  # Save the credentials for the next run
  with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
  return build(API_SERVICE_NAME, API_VERSION, credentials=creds)


def get_my_playlists_list(youtube):
  playlists_req = youtube.playlists().list(
      mine=True,
      part='snippet',
      maxResults=50
  )
  items = []
  while playlists_req:
      playlists_resp = playlists_req.execute()
      items.extend(playlists_resp['items'])
      playlists_req = youtube.playlists().list_next(
          playlists_req, playlists_resp)
  return items


def get_playlists_videos(youtube, playlists):
  for x in playlists:
    x['items'] = get_playlist_videos(youtube, x['id'])
  return playlists


def get_playlist_videos(youtube, pl_id):
  playlistitems_list_request = youtube.playlistItems().list(
      playlistId=pl_id,
      part='snippet,contentDetails',
      maxResults=50
  )
  items = []
  while playlistitems_list_request:
    playlistitems_list_response = playlistitems_list_request.execute()
    items.extend(playlistitems_list_response['items'])
    playlistitems_list_request = youtube.playlistItems().list_next(
        playlistitems_list_request, playlistitems_list_response)
  return items


def get_liked_playlist(youtube):
  # Get likes playlist id
  response = youtube.channels().list(part='contentDetails', mine=True).execute()
  id_likes = response['items'][0]['contentDetails']['relatedPlaylists']['likes']
  return id_likes


def get_liked_videos(youtube):
  request = youtube.videos().list(
      part='snippet,localizations',
      myRating='like',
      maxResults=50
  )
  items = []
  while request:
    response = request.execute()
    items.extend(response['items'])
    request = youtube.videos().list_next(request, response)
  return items


def fix_liked_videos(videos):
  for x in videos:
    snippet = x['snippet']
    # Not used because: snippet.localized.description == snippet.description, snippet.localized.title == snippet.title
    del snippet['localized']
    if 'defaultLanguage' in snippet and not snippet['defaultLanguage'].startswith('en'):
      localizations = x['localizations']
      for loc in localizations:
        if loc.startswith('en'):
          # Use English localization title and description
          snippet['title'] = localizations[loc]['title']
          snippet['description'] = localizations[loc]['description']
          del x['localizations']
          break
        else:
          snippet['description'] = snippet['description'][:10] + '(...)'


def prepare_dir():
  dir_name = 'out'
  if os.path.exists(dir_name) and not os.path.isdir(dir_name):
    dir_name = '.'
  else:
    os.makedirs(dir_name, exist_ok=True)
  return dir_name


if __name__ == '__main__':
  if sys.version_info[0] < 3:
    raise Exception('Must be using Python 3')
  try:
    youtube = get_authenticated_service()
    playlists = get_my_playlists_list(youtube)
    if playlists:
      likes_playlist = get_liked_playlist(youtube)
      playlists.append(
          {'id': likes_playlist, 'snippet': {'title': 'Liked videos'}})
      videos = get_playlists_videos(youtube, playlists)
      time_str = datetime.now().strftime('%Y-%m-%d.%H-%M-%S')
      file_path = os.path.join(prepare_dir(), f'response.{time_str}.json')
      with open(file_path, 'w') as f:
        f.write(json.dumps(videos, sort_keys=True))
        print('Wrote', file_path)
    else:
      print('There is no uploaded videos playlist for this user.')
  except HttpError as e:
    print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
