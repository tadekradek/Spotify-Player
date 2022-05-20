import spotipy as spot
import tkinter as tk
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
def Spotify(): # gathers credentials required to connect with spotify account - client id, client secret token and uri
    df=pd.read_csv('key.csv')
    credentials=spot.Spotify(auth_manager=SpotifyOAuth(client_id=df['clientid'].values[0],client_secret=df['clientsecret'].values[0],redirect_uri=df['uri'].values[0],scope=scope))
    return(credentials)

# Spotify() function will be used  EVERY SINGLE TIME when any element from Spotify will be required
results=Spotify().current_user_playlists()

def SelectPlaylistAndPlaylistID(): #obtains playlists names available for current user
    playlist_names=[]
    playlist_id=[]
    for x in range(0,len(results['items'])):
        playlist_names.append(results['items'][x]['name'])
        playlist_id.append(results['items'][x]['id'])

    return([playlist_names,playlist_id])    

playlist=SelectPlaylistAndPlaylistID()
temp_playlist_id=playlist[1][1]

play_selected_playlist=Spotify().playlist(temp_playlist_id)
Spotify().start_playback(device_id="0c3c7767a7157e925aed5d8d907f2e693020161a",context_uri="spotify:playlist:70xamtzn4Kn7tPPBaTjGX6")
#def SongsForSelectedPlaylists():
Spotify().current_playback()
#results=Spotify().current_user_playlists()0c3c7767a7157e925aed5d8d907f2e693020161a
#results['items']
#type(results['items']) #list
#type(results['items'][0]) # every item (playlist) is a dictionary
#type(results['items'][0]['name']) #final name of the playlist

print(temp_playlist_id)





