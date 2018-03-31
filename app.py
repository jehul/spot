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



playlists={}
for i, item in enumerate(user_playlists['items']):
	print("%d %s" %(i, item['name']))
	playlists[item['name']] = 1

with open('playlists.txt', 'w') as outfile:  
    json.dump(playlists, outfile)

selected_playlist_number = input('Select a playlist to analyze (playlist number):')

#Gets songs from selected playlist
playlist_uri = user_playlists['items'][int(selected_playlist_number)]['uri']
playlist_id = playlist_uri.split(':')[4]
songs = sp.user_playlist(username, playlist_id)['tracks']['items']

#Get unique country codes in playlist
countries_in_playlist = {}
for i, item in enumerate(songs):
	for j in item['track']['available_markets']:
		if j not in countries_in_playlist:
			countries_in_playlist[j] = 1

#output JSON with unique country codes
with open('countries.txt', 'w') as outfile:  
    json.dump(countries_in_playlist, outfile)



#Get feature vectors for each song
feature_dict = {}
for i, item in enumerate(songs):
	track_id = item['track']['id']
	features = sp.audio_features(track_id)
	feature_dict[i] = features
	
with open('playlist_features.txt', 'w') as outfile:  
    json.dump(feature_dict, outfile)

#Get feature vectors for a user's library
"""
if token:
	library = sp.current_user_saved_tracks()
	while library['next'] != None:
		print(json.dumps(library, sort_keys=True, indent=4))
		library = 

"""

#print(json.dumps(VARIABLE, sort_keys=True, indent=4))



