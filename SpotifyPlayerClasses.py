import base64
from random import random
from select import select
from turtle import width
import requests
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import os
import pandas as pd
import random
import unidecode
import difflib
import tkinter as tk
from tkinter import END, ttk 
from tkinter.messagebox import showinfo
from PIL import Image
import requests
import time

class NewGame():

    def __init__(self, keys):
        self.df = pd.read_csv(keys)
        self.device_id = self.df['deviceid'].values[0]
        self.client_id = self.df['clientid'].values[0]
        self.client_secret = self.df['clientsecret'].values[0]
        self.redirect_uri = self.df['redirecturi'].values[0]
        self.open_spotify_app()
        self.spotify = NewGame.spotify(self)
        self.list_of_songs = []
        self.selected_song = []
        self.song_details = []
        self.playlists_names_and_id =[]
        self.playlists_only = []
        self.selected_playlist = ""
        self.comparison_response = tk.StringVar()
        self.comparison_response.set("Temp")
        self.user_playlists_names_and_id()
        self.entry_playlist_variable = tk.StringVar()
        self.entry_playlist_variable.set(self.playlist_names_only[0])
        
        self.correctly_recognized = 0
        self.skipped = 0
        self.incorrect = 0

        self.initial_message_label = ttk.Label(root, text= "Welcome in Spotify Trivia! \nPlease select playlist from dropdown box and press submit button.")
        self.entry_dropdown_playlist = ttk.Combobox(root, textvariable = self.entry_playlist_variable, values = self.playlist_names_only, state ='readonly')
        self.submit_entry_playlist_button = ttk.Button(root, text= "Submit chosen playlist", command = lambda:[self.entry_dropdown_playlist.forget(),
                                                                                                              self.submit_entry_playlist_button.forget(),
                                                                                                              self.initial_message_label.forget(),
                                                                                                              self.user_selected_playlist(self.entry_playlist_variable.get()),
                                                                                                              self.list_of_songs_from_selected_playlist(self.selected_playlist), #till this moment it works
                                                                                                              
                                                                                                              self.start_the_game_button.pack()
                                                                                                              ])
        self.start_the_game_button = ttk.Button(root, text = "Lets start the game!", command = lambda:[self.select_random_song(),
                                                                                                       self.current_song_details(),
                                                                                                       self.play_song_from_start(),
                                                                                                       self.start_the_game_button.forget(),
                                                                                                       self.reset_game_stats(),
                                                                                                       self.pause_button.pack(),
                                                                                                       self.restart_button.pack(),
                                                                                                       self.answer_text_entry.pack(),
                                                                                                       self.submit_answer_button.pack(),
                                                                                                       self.skip_button.pack()
                                                                                                       ])
        self.resume_button = ttk.Button(root, text= "Resume Song", command = lambda:[self.resume_song(),
                                                                                     self.resume_button.forget(),
                                                                                     self.pause_button.forget(),
                                                                                     self.restart_button.pack(),
                                                                                     self.skip_button.pack(),
                                                                                     self.pause_button.pack()
                                                                                     ])
        self.pause_button = ttk.Button(root, text= "Pause song", command =lambda:[self.pause_song(),
                                                                                  self.pause_button.forget(),
                                                                                  self.restart_button.forget(),
                                                                                  self.resume_button.pack(),
                                                                                  self.skip_button.forget()
                                                                                  
                                                                                  ])
        self.restart_button = ttk.Button(root, text= "Restart song", command = lambda:[self.play_song_from_start(),
                                                                                       self.pause_button.pack()
                                                                                       ])
        self.answer_text_entry = ttk.Entry(root)
        self.submit_answer_button = ttk.Button(root, text = "Submit your answer", command= lambda:[self.compare_artist(self.answer_text_entry.get()),
                                                                                                   self.comparison_result_label_build(),
                                                                                                   self.submit_answer_button.forget()
                                                                                                   ])

        self.retry_button = ttk.Button(root, text=" Retry", command= lambda:[self.answer_text_entry.delete(0,END),
                                                                             self.comparison_result_label.destroy(),
                                                                             self.retry_button.forget(),
                                                                             self.submit_answer_button.pack()
                                                                             
                                                                             
        ])

        self.play_next_song_button = ttk.Button(root, text="Play Next Song", command=lambda:[self.details_display_hide(),
                                                                                             self.select_random_song(),
                                                                                             self.current_song_details(),
                                                                                             self.play_song_from_start(),
                                                                                             self.play_next_song_button.forget(),
                                                                                             self.comparison_result_label.destroy(),
                                                                                             self.answer_text_entry.delete(0,END),
                                                                                             self.submit_answer_button.pack(),
                                                                                             self.skip_button.pack()

        ])

        self.skip_button = ttk.Button(root, text =  "Skip the song", command= lambda:[self.skip_song(root)])
        self.initial_message_label.pack()
        self.entry_dropdown_playlist.pack()
        self.submit_entry_playlist_button.pack()
        
    def open_spotify_app(self):
        """
        command to open Spotify application, please adjust the path in order to run it on your version

        """
        os.startfile("C:\\Users\Radek\Desktop\Spotify.lnk") #to make in more generic, either enter the path as paramater in the function or at least leave area where user can define it

    def spotify(self):
        """
        gathers credentials required to connect with spotify account - client id, client secret token and uri
        please note that you have to have a premium account active to be able to use Spotify API
        in addition, in order not to provide the key in open source, it is being read from a locally attached file
        defining this function allows to access Spotify methods from spotipy module
        """
        scope = 'user-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-collaborative'
        
        credentials = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,client_secret=self.client_secret,redirect_uri=self.redirect_uri,scope=scope))
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
        for i in range (0, len(self.spotify.track(self.selected_song[0])['artists'])):
            song_artists.append(self.spotify.track(self.selected_song[0])['artists'][i]['name'])

        song_year = self.spotify.track(self.selected_song[0])['album']['release_date']
        
        song_album_title = self.spotify.track(self.selected_song[0])['album']['name']

        song_title = self.spotify.track(self.selected_song[0])['name']

        song_photo = self.spotify.track(self.selected_song[0])['album']['images'][0]['url']
        
        self.song_details = [song_title, song_artists, song_year, song_album_title, song_photo]
        
    def play_song_from_start(self):
        self.spotify.start_playback(device_id = self.device_id, uris = self.selected_song)
        
    def resume_song(self):
        self.spotify.start_playback(device_id = self.device_id, uris = self.selected_song, position_ms = self.spotify.current_playback()["progress_ms"])

    def pause_song(self):
        self.spotify.pause_playback(device_id = self.device_id)

    def compare_artist(self, artist_answer):
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
            self.comparison_response.set("Excellent!")
            self.correctly_recognized = self.correctly_recognized + 1
            self.details_display_label(root)
            self.play_next_song_button.pack()

        elif max(sequence_matcher_ratio) < 1 and max(sequence_matcher_ratio) >= 0.70 and len(correct_answers[sequence_matcher_ratio.index(max(sequence_matcher_ratio))]) == len(artist_answer): 
            self.incorrect = self.incorrect + 1
            counter = 0
            correct_char = [*correct_answers[sequence_matcher_ratio.index(max(sequence_matcher_ratio))]]
            ans_char = [*artist_answer]
            for x in range (0, len(artist_answer)):
                if correct_char[x] != ans_char[x]:
                    counter = counter + 1

            if counter == 1:
                self.comparison_response.set("There is exactly one typo, try again!")
                self.retry_button.pack() 
            elif counter == 2:
                self.comparison_response.set("There are exactly two typos, try again.")
                self.retry_button.pack() 
            else:
                self.comparison_response.set("There are three or even more typos, but number of characters is still correct.")
                self.retry_button.pack()

        elif max(sequence_matcher_ratio) < 1 and max(sequence_matcher_ratio) >= 0.80 and abs(len(correct_answers[sequence_matcher_ratio.index(max(sequence_matcher_ratio))]) != len(artist_answer)):
            self.incorrect = self.incorrect + 1
            self.comparison_response.set("Its quite close, but number of characters in correct answer is different.") 
            self.retry_button.pack()
        else:
           self.incorrect = self.incorrect + 1 
           self.comparison_response.set("Incorrect!")
           self.retry_button.pack() 

    def widget_pack(self, widget):
        widget.pack()

    def widget_forget(self, widget):
        widget.forget()

    def supportive_label(self, root):
        self.supportive_label = ttk.Label(root, text = self.selected_playlist)
        self.widget_pack(self.supportive_label)

    def comparison_result_label_build(self):
        self.comparison_result_label = ttk.Label(root, text = self.comparison_response.get())
        self.comparison_result_label.pack()
    
    def details_display_label(self,root):
        self.song_artists_label = ttk.Label(root, text = "Artist(s): {}".format(self.song_details[1]))
        self.song_title = ttk.Label(root, text = "Song Title: {}".format(self.song_details[0]))
        self.song_album = ttk.Label(root, text = "Album: {}".format(self.song_details[3]))
        self.song_year = ttk.Label(root, text = "Released: {}".format(self.song_details[2]))
        self.song_artists_label.pack()
        self.song_title.pack()
        self.song_album.pack()
        self.song_year.pack()

    def details_display_hide(self):
        self.song_artists_label.forget()
        self.song_title.forget()
        self.song_album.forget()
        self.song_year.forget()

    def reset_game_stats(self):
        self.correctly_recognized = 0
        self.skipped = 0
        self.incorrect = 0

    def skip_song(self, root):
        self.pause_song()
        self.details_display_label(root)
        self.skipped = self.skipped + 1
        self.play_next_song_button.pack()


root = tk.Tk()
root.title("Spotify Music Trivia")
screen_width = root.winfo_screenwidth() #1536 on laptop
screen_height = root.winfo_screenheight() #864 on laptop
root.geometry(f"{int(0.8*screen_width)}x{int(0.8*screen_height)}+{int(0.1*screen_width)}+{int(0.1*screen_height)}")
root.resizable(False,False)
root.configure(bg="#828282")

new_game = NewGame('keys.csv')

#new_game.create_entry_dropdown_button(root)

root.mainloop()



Spotify().track('spotify:track:2AMysGXOe0zzZJMtH3Nizb')['album']['images'][0]['url']

def Spotify(): # gathers credentials required to connect with spotify account - client id, client secret token and uri
    df=pd.read_csv('keys.csv')
    scope = 'user-read-private user-read-playback-state user-modify-playback-state'
    credentials=spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=df['clientid'].values[0],client_secret=df['clientsecret'].values[0],redirect_uri=df['redirecturi'].values[0],scope=scope))
    return(credentials)

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