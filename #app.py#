import spotipy
import os
import sys
import json
import webbrowser
import spotipy.util as util
#from json.decoder import JSONDecodeError


#Get username 1253897466
username = sys.argv[1]
scope = 'user-library-read'

try:
	token = util.prompt_for_user_token(username,scope)
except:
	os.remove(f".cache-{username}")
	token = util.prompt_for_user_token(username,scope)

#token = util.prompt_for_user_token(username,scope)

#Create spotify object 
sp = spotipy.Spotify(auth=token)
user = sp.current_user()

#Print Introduction
display_name = user['display_name']
num_followers = user['followers']['total']

print(">>>Welcome " + display_name + "!")
print(">>>You have " + str(num_followers) + " followers.")
print()


#Print Playlists
print(">>>Here are your playlists!")
user_playlists = sp.current_user_playlists(limit=50)
for i, item in enumerate(user_playlists['items']):
	print("%d %s" %(i, item['name']))

selected_playlist_number = input('Select a playlist to analyze (playlist number):')

#Gets songs from selected playlist
playlist_uri = user_playlists['items'][int(selected_playlist_number)]['uri']
playlist_id = playlist_uri.split(':')[4]
songs = sp.user_playlist(username, playlist_id)['tracks']['items']


#Get feature vectors for each song
for item in songs:
	track_id = item['track']['id']
	features = sp.audio_features(track_id)
	print(json.dumps(features, sort_keys=True, indent=4))

#print(json.dumps(VARIABLE, sort_keys=True, indent=4))



