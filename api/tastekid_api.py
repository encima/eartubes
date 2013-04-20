import urllib2
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
    artists = artists.split(", ")
    params = {}
    for movie in movies:
      movie = movie.replace(" ", "+")
      params[movie] = 'movie'
    return self.api_call(params, 'movies', False)

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
    return json.dumps(response)

#t = TastekidApi('hans+zimmer')
#print t.get_similar_movies_from_artists('hans zimmer, hank williams')
