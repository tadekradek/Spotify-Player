from logging import root
from re import I
import spotipy as spot
import tkinter as tk
from tkinter import ttk
import pandas as pd
import time
import random
import unidecode


from tkinter.messagebox import showinfo
from spotipy.oauth2 import SpotifyOAuth
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
def Spotify(): # gathers credentials required to connect with spotify account - client id, client secret token and uri
    df=pd.read_csv('key.csv')
    credentials=spot.Spotify(auth_manager=SpotifyOAuth(client_id=df['clientid'].values[0],client_secret=df['clientsecret'].values[0],redirect_uri=df['uri'].values[0],scope=scope))
    return(credentials)

# Spotify() function will be used  EVERY SINGLE TIME when any element from Spotify will be required

def CurrentUserPlaylists():
    return Spotify().current_user_playlists()

##### this function obtains playlist of CURRENT USER
def SelectPlaylistAndPlaylistID(): #obtains playlists names available for current user
    playlists=Spotify().current_user_playlists()
    playlist_names=[]
    playlist_id=[]
    for i in range(0,len(playlists['items'])):
        playlist_names.append(playlists['items'][i]['name'])
        playlist_id.append(playlists['items'][i]['id'])
    return([playlist_names,playlist_id])    

selectedPlaylistNamesAndId=SelectPlaylistAndPlaylistID() ## global variable 


#### this function obtains playlist of SELECTED USER, based on the user id
#def SelectPlaylistAndPlaylistID(): #obtains playlists names available for current user
#    playlists=Spotify().user_playlists("21dpuynr2j4jckz3seeogxzwq")
#    playlist_names=[]
#    playlist_id=[]
#    for i in range(0,len(playlists['items'])):
#        playlist_names.append(playlists['items'][i]['name'])
#        playlist_id.append(playlists['items'][i]['id'])
#   return([playlist_names,playlist_id])    



selectedPlaylistName='Billboard 2001'

def selectPlaylistUri(x,y):
    """
    :param x: (list) the list containing [[name],[id]] of all available user's playlists

    :param y: (string) name of list selected based on dropdown list in the application
    """
    selectedPlaylistUri=[]
    for i in range (0,len(x[0])):
        if x[0][i] == y:
            selectedPlaylistUri.append(x[1][i])
            break
    return x[1][i]

selectPlaylistUri(selectedPlaylistNamesAndId,'Billboard 2001' )
selectPlaylistUri(selectedPlaylistNamesAndId) ## returns the uri of playlist selected by user


def playbackSelectedPlaylist(playlistUri):
    """
    :param playlistUri: string of uri of selected playlists that will be used to gather individual songs
    """
    return Spotify().playlist(playlistUri)

type(playbackSelectedPlaylist('53mEQlZ91fLxuSOo048KFc'))
selectedPlaylist=Spotify().playlist('53mEQlZ91fLxuSOo048KFc')

selectedPlaylist["tracks"]["items"]

def ListOfSongsToPlayback(x):

    """
    :param x: dictionary containing currently selected playlist
    :return: returns a list of uri with all tracks in the list
    """
    #dict_keys(['collaborative', 'description', 'external_urls', 'followers', 'href', 'id', 'images', 'name', 'owner', 'primary_color', 'public', 'snapshot_id', 'tracks', 'type', 'uri'])
    #play_selected_playlist["tracks"]["items"][0]["track"]["name"] #### to capture the title of the song

    uniqueUrisCollected=[]
    for i in range(0,len(x["tracks"]["items"])):
        uniqueUrisCollected.append(x["tracks"]["items"][i]["track"]["uri"])
    return (uniqueUrisCollected)
 

currentPlaylist=ListOfSongsToPlayback(Spotify().playlist('53mEQlZ91fLxuSOo048KFc'))

#currentPlaylist=ListOfSongsToPlayback() #freshly obtained list of all tracks from the selected list
#len(currentPlaylist)
def selectRandomSong(x):
    """
    :param x: (List) with all songs currently stored in the global variable
    """
    selectedSong=[]
    selectedSong.append(random.choice(x))
    x.remove(selectedSong[0])
    print(len(currentPlaylist))
    return selectedSong[0]


     # line to select random element from the list
len(currentPlaylist)
currentSong=selectRandomSong(currentPlaylist)


 #removing song once selected

def getCurrentSongDetails(x):
    """
    :param x: (string) uri of currently selected song
    """
    song=Spotify().current_playback()
    details=[[],[],[],[],[]]
    #details[0] - song title
    details[0].append(song["item"]["name"])
    #details[1] - artists
    for i in range (0, len(song["item"]["artists"])):
        details[1].append(song["item"]["artists"][i]["name"])
    #details[2] - release date


    details[2].append(song["item"]["album"]["release_date"][0:4])
    #details[3] - album title
    details[3].append(song["item"]["album"]['name'])
    #details[4] - album artists
    for i in range (0, len(song["item"]["album"]["artists"])):
        if len(details[4])==0:
            details[4].append(song["item"]["artists"][i]["name"])
        else:
            details[4][0]=details[4][0]+ ", {}".format(song["item"]["artists"][i]["name"])
            
    return details

currentSongDetails=getCurrentSongDetails(currentSong)
x=currentSongDetails[1]
x
y="Vanessą Ćarlton"
def guessTheArtist(x,y):
    for i in range(0,len(x)):
        x[i]=unidecode.unidecode(x[i])
        x[i].lower()
    y=unidecode.unidecode(y)
    y.lower()
    if y in x:
        print("Correct")
    else:
        print("Incorrect!")  
        


#Spotify().start_playback(device_id="0c3c7767a7157e925aed5d8d907f2e693020161a",uris=["spotify:track:02RqhFaAYzWScfVzKfTZ7L"])

#time.sleep(3)
#Spotify().start_playback(device_id="0c3c7767a7157e925aed5d8d907f2e693020161a",uris=["spotify:track:45evHLPMTNicGtSbsUvgjN"])

#context_uri="spotify:playlist:70xamtzn4Kn7tPPBaTjGX6"
#def SongsForSelectedPlaylists():
Spotify().current_playback()
def playSelectedSong():
    Spotify().start_playback(device_id=Spotify().current_playback()["device"]["id"],uris=[currentSong[0]])

def playSongFromStart():
    Spotify().start_playback(device_id=Spotify().current_playback()["device"]["id"],uris=[Spotify().current_playback()["item"]["uri"]])
    
def resumeSong():
    Spotify().start_playback(device_id=Spotify().current_playback()["device"]["id"],uris=[Spotify().current_playback()["item"]["uri"]],position_ms=Spotify().current_playback()["progress_ms"])

def pauseSong():
    Spotify().pause_playback(device_id=Spotify().current_playback()["device"]["id"])


Spotify().user_playlists("21dpuynr2j4jckz3seeogxzwq")
################################# tkinter core ######################

window = tk.Tk()
window.title('Spotify Player')
window.geometry('600x600+100+100') #width x heigt + translation where the app is displayed every time it is runned
#window.attributes('-fullscreen', True) alternatively running in full screen mode, but there's no 'x' to quickly kill it so altf4 neeeded

#play, pause and resume buttons
button_Play = tk.Button(text="Play From Start",command=playSongFromStart)
button_Pause = tk.Button(text="Pause Song",command=pauseSong)
button_Resume = tk.Button(text="Resume Song",command=resumeSong)
#button_Play.pack()
#button_Pause.pack()
#button_Resume.pack()


class Test():
   def __init__(self):
       self.root = tk.Tk()
       self.title('Spotify Player')
       self.geometry('600x600+100+100')
       self.label=tk.Label(self.root,
                           text = "Label")
       self.buttonForget = tk.Button(self.root,
                          text = 'Click to hide Label',
                          command=lambda: self.label.pack_forget())
       self.buttonRecover = tk.Button(self.root,
                          text = 'Click to show Label',
                          command=lambda: self.label.pack())       
       
       self.buttonForget.pack()
       self.buttonRecover.pack()
       self.label.pack(side="bottom")
       self.root.mainloop()

   def quit(self):
       self.root.destroy()
        

app=Test()
button_Welcome = tk.Button(window,text="Welome to Spotify Music Quiz!")
button_Welcome.pack()

#entry list to select the initial playlist to play
#SelectPlaylistAndPlaylistID()[0][0]
variable=tk.StringVar()
variable.set(SelectPlaylistAndPlaylistID()[0][0])
drop=ttk.Combobox(window,textvariable=variable,values=SelectPlaylistAndPlaylistID()[0])
#drop.pack()




label=tk.Label(textvariable=variable)
#label.pack()

window.mainloop()

#def ListChanged(event):
#    """ handle the month changed event """
#    showinfo(
#        title='Result',
#        message=f'You selected {variable.get()}!'
#    )
#drop.bind('<<ComboboxSelected>>',ListChanged)