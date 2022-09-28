from random import random
from select import select
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import os
import pandas as pd
import random
import unidecode
import difflib

def Spotify():
    """
    gathers credentials required to connect with spotify account - client id, client secret token and uri
    please note that you have to have a premium account active to be able to use Spotify API
    in addition, in order not to provide the key in open source, it is being read from a locally attached file
    defining this function allows to access Spotify methods from spotipy module
    """
    scope = 'user-read-private user-read-playback-state user-modify-playback-state'
    df = pd.read_csv('key.csv')
    credentials = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=df['clientid'].values[0],client_secret=df['clientsecret'].values[0],redirect_uri=df['uri'].values[0],scope=scope))
    return(credentials)

def open_spotify_app():
    """
    command to open Spotify application, please adjust the path in order to run it on your version
    """
    os.startfile("C:\\Users\Radek\Desktop\Spotify.lnk")

def user_playlists_names_and_id():
    """
    This functions returns name and id of every playlist that is available for the user
    the output contains list of two-element lists (name and id)
    """
    playlist_names_and_id = []
    for x in range(0, len(Spotify().current_user_playlists()["items"])):
        playlist_names_and_id.append([Spotify().current_user_playlists()["items"][x]['name'], Spotify().current_user_playlists()["items"][x]['id']])
    return playlist_names_and_id

def uri_of_selected_playlist(selected_name):
    """
    :param selected name: (string) name of playlist selected by the player
    based on the provided name of playlist (selected by user from dropdown list),
    this function returns the uri code of selected playlist
    """
    for x in range(0, len(user_playlists_names_and_id())):
        if user_playlists_names_and_id()[x][0] == selected_name:
            return user_playlists_names_and_id()[x][1]

def list_of_songs_from_selected_playlist(selected_playlist_uri):
    """
    :param selected_playlist_uri: (string) uri code of playlist selected by the player
    functions outputs a list containing all tracks from the playlist selected based on uri provided as argument
    """
    list_of_songs = []
    for x in range (0, len(Spotify().playlist_items(selected_playlist_uri)["items"])):
        list_of_songs.append(Spotify().playlist_items(selected_playlist_uri)["items"][x]["track"]["uri"])
    return list_of_songs

list_of_songs = list_of_songs_from_selected_playlist(uri_of_selected_playlist("Onetricki"))

def select_random_song(selected_list):
    """
    :param selected_list: (list) list of songs from currently selected playlist
    function selects random song from the list of songs provided as parameter, removes it from this list and returns the song uri
    """
    currentSong = []
    currentSong.append(random.choice(list))
    list.remove(currentSong[0])
    return currentSong
    

def current_song_details():
    """
    this function captures the details related to song currently loaded in player and returns a list
    """
    song_title = Spotify().current_playback()["item"]["name"]

    song_artists = []
    for i in range (0, len(Spotify().current_playback()["item"]["artists"])):
        song_artists.append(Spotify().current_playback()["item"]["artists"][i]["name"])

    song_year = Spotify().current_playback()["item"]["album"]["release_date"][0:4]
    
    song_album_title = Spotify().current_playback()["item"]["album"]['name']
    
    return [song_title, song_artists, song_year, song_album_title]

#def playSelectedSong():
#    Spotify().start_playback(device_id=Spotify().current_playback()["device"]["id"],uris=)

def playSongFromStart():
    Spotify().start_playback(device_id=Spotify().current_playback()["device"]["id"],uris=[Spotify().current_playback()["item"]["uri"]])
    
def resumeSong():
    Spotify().start_playback(device_id=Spotify().current_playback()["device"]["id"],uris=[Spotify().current_playback()["item"]["uri"]],position_ms=Spotify().current_playback()["progress_ms"])

def pauseSong():
    Spotify().pause_playback(device_id=Spotify().current_playback()["device"]["id"])

def compareArtist(artist_answer):
    """
    :param artist_answer: (string) answer provided by player in order to guess the artist
    function compares the correct artist/artists covering the currently selected song with the answer provided by user
    based on the accuracy of answer, it returns different kind of output
    """
    correct_answers = []
    for i in range (0, len(current_song_details()[1])):
        correct_answers.append((unidecode.unidecode(current_song_details()[1][i])).lower())

    artist_answer = unidecode.unidecode(artist_answer.lower())
    artist_answer = artist_answer.strip()
    sequence_matcher_ratio = []
    for i in range (0, len(correct_answers)):
        sequence_matcher_ratio.append(difflib.SequenceMatcher(None, correct_answers[i], artist_answer).ratio())
    
    print(sequence_matcher_ratio)

    if max(sequence_matcher_ratio) == 1:
        print( "Excellent!" )

    elif max(sequence_matcher_ratio) < 1 and max(sequence_matcher_ratio) >= 0.70 and len(correct_answers[sequence_matcher_ratio.index(max(sequence_matcher_ratio))]) == len(artist_answer): 
        counter = 0
        correct_char = [*correct_answers[sequence_matcher_ratio.index(max(sequence_matcher_ratio))]]
        ans_char = [*artist_answer]
        for x in range (0, len(artist_answer)):
            if correct_char[x] != ans_char[x]:
                counter = counter + 1

        if counter == 1:
            print( "There is exactly one typo, try again!" )
        elif counter == 2:
            print( "There are exactly two typos, try again." )
        else:
            print( "There are three or even more typos, but number of characters is still correct.")

    elif max(sequence_matcher_ratio) < 1 and max(sequence_matcher_ratio) >= 0.80 and abs(len(correct_answers[sequence_matcher_ratio.index(max(sequence_matcher_ratio))]) != len(artist_answer)):
        print("Its quite close, but number of characters in correct answer is different.")

    else:
        print( "Incorrect!" )



abs(-3)
     
compareArtist("Quzzbonafide")
"zzzzQuebonafide"
"Quebonafide"
select_random_song(list_of_songs)
len(list_of_songs)



Spotify().start_playback(device_id=Spotify().devices()['devices'][0]["id"], uris=['spotify:track:5VYTKiOnHw4iTrB9pG3yum'])
Spotify()._append_device_id
Spotify().devices()['devices'][0]["id"]

list_of_songs

[*'rad ek']