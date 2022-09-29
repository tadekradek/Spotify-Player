from random import random
from select import select
from turtle import width
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import os
import pandas as pd
import random
import unidecode
import difflib
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

class NewGame():

    def __init__(self):
        
        self.open_spotify_app()
        self.spotify = NewGame.spotify()
        self.list_of_songs = []
        self.selected_song = []
        self.song_details = []
        self.playlists_names_and_id =[]
        self.playlists_only = []
        self.selected_playlist = ""
        self.user_playlists_names_and_id()
        self.entry_playlist_variable = tk.StringVar()
        self.entry_playlist_variable.set(self.playlist_names_only[0])
        
        self.initial_message_label = ttk.Label(root, text= "Welcome in Spotify Trivia! \nPlease select playlist from dropdown box and press submit button.")
        self.entry_dropdown_playlist = ttk.Combobox(root, textvariable = self.entry_playlist_variable, values = self.playlist_names_only, state ='readonly')
        self.submit_entry_playlist_button = ttk.Button(root, text= "Submit chosen playlist", command= lambda:[self.widget_forget(self.entry_dropdown_playlist),
                                                                                                              self.widget_forget(self.submit_entry_playlist_button),
                                                                                                              self.widget_forget(self.initial_message_label),
                                                                                                              self.user_selected_playlist(self.entry_playlist_variable.get()),
                                                                                                              self.list_of_songs_from_selected_playlist(self.selected_playlist), #till this moment it works
                                                                                                              self.supportive_label(root),
                                                                                                              self.widget_pack(self.start_the_game_button)
                                                                                                              ])
        self.start_the_game_button = ttk.Button(root, text = "Lets start the game!", command = lambda:[self.select_random_song(),
                                                                                                       self.playSongFromStart(),
                                                                                                       self.current_song_details(),
                                                                                                       self.widget_forget(self.start_the_game_button),
                                                                                                       self.widget_forget(self.supportive_label)
                                                                                                       ])
        self.initial_message_label.pack()
        self.entry_dropdown_playlist.pack()
        self.submit_entry_playlist_button.pack()
        

    def open_spotify_app(self):
        """
        command to open Spotify application, please adjust the path in order to run it on your version

        """
        os.startfile("C:\\Users\Radek\Desktop\Spotify.lnk") #to make in more generic, either enter the path as paramater in the function or at least leave area where user can define it

    def spotify():
        """
        gathers credentials required to connect with spotify account - client id, client secret token and uri
        please note that you have to have a premium account active to be able to use Spotify API
        in addition, in order not to provide the key in open source, it is being read from a locally attached file
        defining this function allows to access Spotify methods from spotipy module
        """
        scope = 'user-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-collaborative'
        df = pd.read_csv('key.csv')
        credentials = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=df['clientid'].values[0],client_secret=df['clientsecret'].values[0],redirect_uri=df['uri'].values[0],scope=scope))
        return(credentials)

    def user_playlists_names_and_id(self):
        """
        This functions returns name and id of every playlist that is available for the user
        the output contains list of two-element lists (name and id) and another list, containing names only
        """
        self.playlist_names_and_id = []
        self.playlist_names_only = []
        for x in range(0, len(self.spotify.current_user_playlists()["items"])):
            self.playlist_names_and_id.append([self.spotify.current_user_playlists()["items"][x]['name'], self.spotify.current_user_playlists()["items"][x]['id']])
            self.playlist_names_only.append(self.spotify.current_user_playlists()["items"][x]['name'])

    def user_selected_playlist(self, selected_playlist):   
        """
        :param selected name: (string) name of playlist selected by the player
        based on the provided name of playlist (selected by user from dropdown list),
        this function returns the uri code of selected playlist
        """
        for x in range(0, len(self.playlist_names_and_id)):
            if self.playlist_names_and_id[x][0] == selected_playlist:
                self.selected_playlist = self.playlist_names_and_id[x][1]
                print(self.selected_playlist)
                break
            
    def list_of_songs_from_selected_playlist(self, selected_playlist_uri):
        """
        :param selected_playlist_uri: (string) uri code of playlist selected by the player
        functions outputs a list containing all tracks from the playlist selected based on uri provided as argument
        """
        self.list_of_songs = []
        for x in range (0, len(self.spotify.playlist_items(selected_playlist_uri)["items"])):
            self.list_of_songs.append(self.spotify.playlist_items(selected_playlist_uri)["items"][x]["track"]["uri"])
        print(self.list_of_songs)

    def select_random_song(self):
        """
        :param selected_list: (list) list of songs from currently selected playlist
        function selects random song from the list of songs provided as parameter, removes it from this list and returns the song uri
        """
        self.selected_song = []
        self.selected_song.append(random.choice(self.list_of_songs))
        self.list_of_songs.remove(self.selected_song[0])
        
    def current_song_details(self):
        """
        this function captures the details related to song currently loaded in player and returns a list
        """
        self.song_details = []

        song_artists = []
        for i in range (0, len(self.spotify.current_playback()["item"]["artists"])):
            song_artists.append(self.spotify.current_playback()["item"]["artists"][i]["name"])

        song_year = self.spotify.current_playback()["item"]["album"]["release_date"][0:4]
        
        song_album_title = self.spotify.current_playback()["item"]["album"]['name']

        song_title = self.spotify.current_playback()["item"]["name"]
        
        self.song_details = [song_title, song_artists, song_year, song_album_title]

    def playSongFromStart(self):
        self.spotify.start_playback(device_id = self.spotify.current_playback()["device"]["id"], uris = self.selected_song)
        
    def resumeSong(self):
        self.spotify.start_playback(device_id = self.spotify.current_playback()["device"]["id"], uris = self.selected_song, position_ms = self.spotify.current_playback()["progress_ms"])

    def pauseSong(self):
        self.spotify.pause_playback(device_id = self.spotify.current_playback()["device"]["id"])

    def compareArtist(self, artist_answer):
        """
        :param artist_answer: (string) answer provided by player in order to guess the artist
        function compares the correct artist/artists covering the currently selected song with the answer provided by user
        based on the accuracy of answer, it returns different kind of output
        """
        correct_answers = []
        for i in range (0, len(self.song_details[1])):
            correct_answers.append((unidecode.unidecode(self.song_details[1][i])).lower())

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

    def widget_pack(self, widget):
        widget.pack()

    def widget_forget(self, widget):
        widget.forget()

    def supportive_label(self, root):
        self.supportive_label = ttk.Label(root, text = self.selected_playlist)
        self.widget_pack(self.supportive_label)


'''
window = ttk.Tk()
window.title('Spotify Player')
window.geometry('1366x768')

window.mainloop()'''





root = tk.Tk()
root.title("Spotify Music Trivia")
screen_width = root.winfo_screenwidth() #1536 on laptop
screen_height = root.winfo_screenheight() #864 on laptop
root.geometry(f"{int(0.8*screen_width)}x{int(0.8*screen_height)}+{int(0.1*screen_width)}+{int(0.1*screen_height)}")
root.resizable(False,False)
root.configure(bg="#828282")

new_game = NewGame()

#new_game.create_entry_dropdown_button(root)

root.mainloop()




root = tk.Tk()

root.title("Spotify Music Trivia")
screen_width = root.winfo_screenwidth() #1536 on laptop
screen_height = root.winfo_screenheight() #864 on laptop
root.geometry(f"{int(0.8*screen_width)}x{int(0.8*screen_height)}+{int(0.1*screen_width)}+{int(0.1*screen_height)}")
root.resizable(False,False)
root.configure(bg="#828282")

#Welcome Label

#frame_welcome.configure()

#label_welcome = ttk.Label(root, text=" Welcome to Spotify Music Quiz")
#label_welcome.pack()

new_game = NewGame()
entry_playlist_variable = tk.StringVar()
entry_playlist_variable.set(new_game.playlist_names_only[0])
playlist_dropdown_list = ttk.Combobox(root, textvariable = entry_playlist_variable, values=new_game.playlist_names_only)
playlist_dropdown_list['state']='readonly'
playlist_dropdown_list.pack()

root.mainloop()


"""
Spotify green color:
Hex color: 	#1DB954
RGB: 	30 215 96
"""
"""
Spotify Black color:
Hex color: 	#191414
RGB: 	25 20 20

"""

"""
Spotify Grey Solid
Hex: #828282
RGB: 130, 130, 130

"""