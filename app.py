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
#print(json.dumps(user, sort_keys=True, indent=4))

display_name = user['display_name']
num_followers = user['followers']['total']

print(">>>Welcome " + display_name + "!")
print(">>>You have " + str(num_followers) + " followers.")
#print(json.dumps(VARIABLE, sort_keys=TRUE, indent=4))