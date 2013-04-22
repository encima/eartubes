import urllib2
import hashlib
import json
import os

class LastFMHandler:
    def __init__(self):
        self.API_KEY = os.environ['LASTFM_API_KEY']
        self.API_SECRET = os.environ['LASTFM_API_SECRET']
        self.API_ROOT = "http://ws.audioscrobbler.com/2.0/"
        self.LAST_FM_AUTH = "http://www.last.fm/api/auth?api_key=d6b7875c6b075a3d0dfd03a15aacd1f0"
    
    #############
    # OUTWARD-FACING METHODS (can generally be called safely from other modules):

    # Get the authorising URL (redirect users to the returned URL to let them authorise)
    # should be called when user wishes to authorise eartub.es with their last.fm account
    def get_request_auth(self):
        return self.LAST_FM_AUTH

    # Authorise eartub.es with LastFM details. 
    # should be called when request made to eartub.es/lastfm_callback (i.e. after authorisation)
    def authenticate_service(self, request):
        # receive the token from last.fm:
        token = request.args.get('token')
        # use this token to make a web service session:
        responseDict = self.api_call("auth.getSession", {'api_key':self.API_KEY, 'token':token})
        if "error" in responseDict:
            return None
	    print type(responseDict)
        session_key = responseDict['session']['key']
        username = responseDict['session']['name']
        return(session_key, username) 

    # Return set of tracks recently played by the specified user
    def get_recentTracks(self, username=None, session_key=None):
        responseDict = self.api_call("user.getRecentTracks", {'user':username, 'api_key':self.API_KEY}) 
        return responseDict
    
    # Return set of tracks loved by the specified user
    def get_lovedTracks(self, username=None, session_key=None):
        responseDict = self.api_call("user.getLovedTracks", {'user':username, 'api_key':self.API_KEY})
        return responseDict

    # Return set of similar tracks to the one specified. Needs the mbid of desired track
    def get_similarTracks(self, username=None, session_key=None, mbid=None):
        responseDict = self.api_call("track.getSimilar", {'mbid':mbid, 'api_key':self.API_KEY})
        return responseDict
    
    # Access API directly by passing a method and a dictionary of parameters
    def api(self, method, params):
        responseDict = self.api_call(method, params)
        return responseDict

    #############
    # INWARD-FACING METHODS (please don't access these directly):

    # make the signature which which to sign API requests (called by api_call())
    def construct_signature(self, method, params):
        keylist = []
        params['method'] = method
        for param in params:
            keylist.append(param)
        keylist.sort()
        sig = ""
        for item in keylist:
            sig = sig+item+params[item]
        sig=sig+self.API_SECRET
        m = hashlib.md5()
        m.update(sig)
        return m.hexdigest()

    # make api_request 
    # method = package.method (str), params = [key1:str1, key2:str2] (dict of strings)
    def api_call(self, method, params):
        api_sig = self.construct_signature(method, params)
        print "SIG: "+api_sig+" "+str(len(api_sig))
        paramString = ""
        for param in params:
            paramString = paramString+"&"+param+"="+params[param]
        request = self.API_ROOT+"?method="+method+paramString+"&api_sig="+api_sig+"&format=json"
        print "REQUEST: "+request
        response = urllib2.urlopen(request).read()
        print "RESPONSE: " +response
        return json.loads(response) # turn JSON into a dict (see individual methods for expected structure)
