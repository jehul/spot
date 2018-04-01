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

with open('playlists.txt', 'w') as outfile:  
    json.dump(user_playlists, outfile)




playlists={}

for i, item in enumerate(user_playlists['items']):
	print("%d %s" %(i, item['name']))
	playlists[item['name']] = 1

with open('playlists.txt', 'w') as outfile:  
    json.dump(playlists, outfile)



#get track ids of a body of music
def get_track_ids(sp, playlist_id, body="playlist", get_availability=False):
	library_feature_dict = {}
	library_track_id = []
	countries_in_playlist = {}
	
	if body == "library":
		library = sp.current_user_saved_tracks(limit=50)

	else:
		library = sp.user_playlist(username, playlist_id)
		library_track_id.append(library['id'])

	if get_availability == True:
		print("triggered")
		for i, item in enumerate(library['tracks']['items']):
			for j in item['track']['available_markets']:
				if j not in countries_in_playlist.values():
					countries_in_playlist[len(countries_in_playlist)] = j
	
	
	
	
	if body == "playlist":
		for item in library['tracks']['items']:
			library_track_id.append(item['track']['id'])
		while library['tracks']['next']:
			library = sp.next(library)
			for item in library['tracks']['items']:
				library_track_id.append(item['track']['id'])
	
	if body == "library":
		for item in library['items']:
			library_track_id.append(item['track']['id'])
		while library['next']:
			library = sp.next(library)
			for item in library['items']:
				library_track_id.append(item['track']['id'])
		
	return library_track_id, countries_in_playlist


#get feature vector returns a dictionary of features
def get_feature_vectors(track_ids):
	feature_list = []
	for i in range(0, len(track_ids), 50):
		features = sp.audio_features(track_ids[i:i+50])
		feature_list.append(features)

	feature_dict={}
	for i, item in enumerate(feature_list):
		feature_dict[i] = item

	return feature_dict

def create_json(feature_dict, name):
	with open(name, 'w') as outfile:  
		json.dump(feature_dict, outfile)

def main():
	selected_playlist_number = input('Select a playlist to analyze (playlist number):')
	


	playlist_uri = user_playlists['items'][int(selected_playlist_number)]['uri']
	playlist_id = playlist_uri.split(':')[4]
	playlist_track_ids, countries_in_playlist = get_track_ids(sp,  playlist_id, body="playlist", get_availability=True)
	

	create_json(countries_in_playlist, name="countries.txt")
	
	#library_track_id, countries_in_library= get_track_ids(sp, playlist_id, body="library")
	#feature_dict = get_feature_vectors(library_track_id)
	#create_json(feature_dict, name="library_features.txt")





#print(json.dumps(VARIABLE, sort_keys=True, indent=4))



if __name__ == '__main__':
    main()