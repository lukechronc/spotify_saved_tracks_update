import sys
import spotipy
import spotipy.util as util
import subprocess

scope = 'user-library-read,user-top-read,playlist-modify-public,playlist-modify-private'
playlist_name = 'Current Saved Tracks'
subprocess.call("./setEnvVar.sh", shell=True)
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope)

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