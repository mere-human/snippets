#!/usr/bin/python

# Retrieve the authenticated user's uploaded videos.
# Sample usage:
# python my_uploads.py

import argparse
import os
import re
import json
import pickle
import os.path

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
  channels_response = youtube.playlists().list(
      mine=True,
      part='snippet'
  ).execute()
  return channels_response['items']


def get_playlist_videos(youtube, playlists):
  for x in playlists:
    print(x)
    # Retrieve the list of videos uploaded to the authenticated user's channel.
    playlistitems_list_request = youtube.playlistItems().list(
        playlistId=x['id'],
        part='snippet',
        maxResults=50
    )
    x['items'] = []
    while playlistitems_list_request:
      playlistitems_list_response = playlistitems_list_request.execute()
      x['items'].extend(playlistitems_list_response['items'])
      playlistitems_list_request = youtube.playlistItems().list_next(
          playlistitems_list_request, playlistitems_list_response)
  return playlists

if __name__ == '__main__':
  youtube = get_authenticated_service()
  try:
    playlists = get_my_playlists_list(youtube)
    if playlists:
      videos = get_playlist_videos(youtube, playlists)
      with open('response.json', 'w') as f:
        f.write(json.dumps(videos, sort_keys=True, indent=4))
    else:
      print('There is no uploaded videos playlist for this user.')
  except HttpError as e:
    print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
