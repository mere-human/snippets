import http.client
import json

class LastfmApi(object):
  API_KEY = '839b2c8e9c6323c499fd797562620a98'

  def __init__(self):
    self.conn = http.client.HTTPConnection('ws.audioscrobbler.com')

  def artist_get_tags(self, artist):
    self.conn.request('GET', '/2.0/?method=artist.gettoptags&artist={}&autocorrect=1&api_key={}&format=json'.format(artist, LastFmApi.API_KEY))
    res = self.conn.getresponse()
    print(res.status, res.reason)
    return res.read()

  def artist_search(self, artist):
    self.conn.request('GET', '/2.0/?method=artist.search&artist={}&limit=5&api_key={}&format=json'.format(artist, LastFmApi.API_KEY))
    res = self.conn.getresponse()
    print(res.status, res.reason)
    return res.read()

def main():
  api = LastfmApi()
  tags_data = api.artist_search('clutch')
  json_parsed = json.loads(tags_data)
  json_pretty = json.dumps(json_parsed, indent=4, sort_keys=True)
  print(json_pretty)

if __name__ == '__main__':
  main()