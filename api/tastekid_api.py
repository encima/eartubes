import urllib2
from imdb_api import IMDBApi as ia
import json

class TastekidApi:
  def __init__(self):
    self.API_ROOT = "http://www.tastekid.com/ask/ws"
    self.API_APP = "eartubes1763"
    self.API_KEY = "mzqzmzg0mmnh"

  def get_similar_movies_from_artists(self, artists):
    artists = artists.split(", ")
    params = {}
    for artist in artists:
      artist = artist.replace(" ", "+")
      params[artist] = 'music'
    return self.api_call(params, 'movies', False)

  def get_similar_movies(self, movies):
    movies = movies.split(", ")
    params = {}
    for movie in movies:
      movie = movie.replace(" ", "+")
      params[movie] = 'movie'
    response = self.api_call(params, 'movies', True)
    resp = json.loads(response)
    films = {}
    if 'Similar' in resp.keys():
      for r in resp['Similar']['Results']:
        names.append(r['Name'])
        imdb = ia()
        films.append(ia.get_info(r['Name']))
    else:
      resp = '{Error:Nothing found or rate exceeded};'
    return resp

  # make call to tastekid
  def api_call(self, params, returnType, verbose):
    paramString = ""
    for param in params:
      paramString += params[param] + ":" + param + ","
    #authenticate
    paramString += "&f=" + self.API_APP + "&k=" + self.API_KEY
    if verbose:
      paramString += "&verbose=1"
    request = self.API_ROOT + "?q=" + paramString + "//" + returnType  + "&format=JSON"
    response = urllib2.urlopen(request).read()
    return response
    # return json.dumps(response)

# t = TastekidApi()
# resp = t.get_similar_movies('titanic')
