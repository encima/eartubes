import urllib2
import json

class IMDBApi:
  def __init__(self):
    self.API_ROOT = "http://imdbapi.org/"

  def get_info(self, movie=None, year=None, limit=1):
    params = {}
    params['title'] = movie
    if year != None:
      params['year'] = year
    params['limit'] = limit
    return self.api_call(params)

  #api calls to IMDB
  def api_call(self, params):
    paramString = "?type=json"
    for param in params:
      paramString += "&" + param + "=" + str(params[param])
    request = self.API_ROOT + "" + paramString
    response = urllib2.urlopen(request).read()
    return response
    # return json.dumps(response)

#ia = IMDBApi()
#print ia.get_info('vanilla', None, 1)
