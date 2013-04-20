import requests
import urllib2
import hashlib
import json

class tastekid_api:
  def __init__(self, artist):
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


  # make call to tastekid
  def api_call(self, params, returnType, verbose):
    paramString = ""
    for param in params:
      print param
      paramString += params[param] + ":" + param + ","
    #authenticate
    paramString += "&f=" + self.API_APP + "&k=" + self.API_KEY
    if verbose:
      paramString += "&verbose=1"
    request = self.API_ROOT + "?q=" + paramString + "//" + returnType  + "&format=JSON"
    print "REQUEST:" + request
    response = urllib2.urlopen(request).read()
    return json.dumps(response)

#t = tastekid_api('hans+zimmer')
#print t.get_similar_movies_from_artists('hans zimmer, hank williams')
