import urllib2
import json

class TMDBApi:
  def __init__(self):
    self.API_ROOT = "http://api.themoviedb.org/3/"
    self.API_KEY = "4cddc3f8f8a7d55bfdf9a90a97ded0e5"

  def get_info(self, movie=None, year=None):
    params = {}
    params['query'] = movie
    if year != None:
      params['year'] = year
    return self.api_call('search/movie', params)

  #api calls to IMDB
  def api_call(self, method, params):
    paramString = "?api_key=" + self.API_KEY
    for param in params:
      paramString += "&" + param + "=" + str(params[param])
    request = self.API_ROOT + "" + method + "" + paramString
    print request
    response = urllib2.urlopen(request).read()
    print response
    # return response
    return json.loads(response)

ta = TMDBApi()
print ta.get_info('vanilla+sky', None)
