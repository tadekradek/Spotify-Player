import spotipy as spot
import tkinter as tk
import pandas as pd
import time
import random
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
temp_playlist_id=playlist[1][3]
play_selected_playlist=Spotify().playlist(temp_playlist_id)

def ListOfSongsToPlayback():
    #dict_keys(['collaborative', 'description', 'external_urls', 'followers', 'href', 'id', 'images', 'name', 'owner', 'primary_color', 'public', 'snapshot_id', 'tracks', 'type', 'uri'])
    #play_selected_playlist["tracks"]["items"][0]["track"]["name"] #### to capture the title of the song
    uniqueUrisCollected=[]
    for i in range(0,len(play_selected_playlist["tracks"]["items"])):
        uniqueUrisCollected.append(play_selected_playlist["tracks"]["items"][i]["track"]["uri"])
    return (uniqueUrisCollected)
    play_selected_playlist["tracks"]["items"][1]["track"]["uri"]  ## collecting unique uri

    play_selected_playlist["tracks"]["items"][0]["track"]["artists"][0]["name"] ## to capture all artists, loop required
    type(play_selected_playlist)


currentPlaylist=ListOfSongsToPlayback() #freshly obtained list of all tracks from the selected list
len(currentPlaylist)
randomSongFromPlaylist=random.choice(currentPlaylist) # line to select random element from the list
currentPlaylist.remove(randomSongFromPlaylist) #removing song once selected
len(currentPlaylist)



#
#Spotify().start_playback(device_id="0c3c7767a7157e925aed5d8d907f2e693020161a",uris=["spotify:track:02RqhFaAYzWScfVzKfTZ7L"])

#time.sleep(3)
#Spotify().start_playback(device_id="0c3c7767a7157e925aed5d8d907f2e693020161a",uris=["spotify:track:45evHLPMTNicGtSbsUvgjN"])

#context_uri="spotify:playlist:70xamtzn4Kn7tPPBaTjGX6"
#def SongsForSelectedPlaylists():
Spotify().current_playback()["item"]["uri"]
def playSelectedSong():
    Spotify().start_playback(device_id=Spotify().current_playback()["device"]["id"],uris=[randomSongFromPlaylist])

def playSongFromStart():
    Spotify().start_playback(device_id=Spotify().current_playback()["device"]["id"],uris=[Spotify().current_playback()["item"]["uri"]])
    
def resumeSong():
    Spotify().start_playback(device_id=Spotify().current_playback()["device"]["id"],uris=[Spotify().current_playback()["item"]["uri"]],position_ms=Spotify().current_playback()["progress_ms"])

def pauseSong():
    Spotify().pause_playback(device_id=Spotify().current_playback()["device"]["id"])



################################# tkinter core ######################

window = tk.Tk()
window.title('Spotify Player')
window.geometry('600x600+100+100') #width x heigt + translation where the app is displayed every time it is runned
#window.attributes('-fullscreen', True) alternatively running in full screen mode, but there's no 'x' to quickly kill it so altf4 neeeded



#def handle_click(event):
#    print("The button was clicked!")

button1 = tk.Button(text="Play From Start",command=playSongFromStart)

button2 = tk.Button(text="Pause Song",command=pauseSong)

button3 = tk.Button(text="Resume Song",command=resumeSong)

#button.bind("<Button-1>", handle_click)

button1.pack()
button2.pack()
button3.pack()

window.mainloop()

