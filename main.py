import sys
import spotipy
import spotipy.util as util
import os.path
import json
class Config:
    __configDict = {}

    def __init__(self, client_id = '', client_secret = '', redirect_uri = ''):
        self.loadConfig()
        self.__configDict['client_id'] = client_id
        self.__configDict['client_secret'] = client_secret
        self.__configDict['redirect_uri'] = redirect_uri
        self.saveConfig()

    def loadConfig(self):
        if os.path.isfile("config.json"):
            f = open("config.json", "r")
            self.__configDict = json.loads(f.read())
            f.close

    def saveConfig(self):
        f = open("config.json", "w+")
        f.write(json.dumps(self.__configDict))
        f.close()

    def get_client_id(self):
        return self.__configDict.get('client_id')

    def set_client_id(self, client_id):
        self.__configDict['client_id'] = client_id
        self.saveConfig()
    
    def get_client_secret(self):
        return self.__configDict.get('client_secret')

    def set_client_secret(self, client_secret):
        self.__configDict['client_secret'] = client_secret
        self.saveConfig()
    
    def get_redirect_uri(self):
        return self.__configDict.get('redirect_uri')

    def set_redirect_uri(self, redirect_uri):
        self.__configDict['redirect_uri'] = redirect_uri
        self.saveConfig()
    
scope = 'user-library-read,user-top-read,playlist-modify-public,playlist-modify-private'
playlist_name = 'Current Saved Tracks'
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()
config = Config("client_id","client_secret","http://localhost:8080")
token = util.prompt_for_user_token(username, scope,client_id=config.get_client_id(),client_secret=config.get_client_secret(),redirect_uri=config.get_redirect_uri())

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_playlists(limit=50)
    for item in results['items']:
        name = item['name']
        if (name == playlist_name):
            id = item['id']
            saved_tracks = sp.current_user_saved_tracks(limit=50)
            tracks = []
            
            for track in saved_tracks['items']:
                tracks.append(track['track']['id'])
            sp.user_playlist_replace_tracks(playlist_id=id,user=username,tracks=tracks)
            sys.exit()

else:
    print("Can't get token for", username)


    
            