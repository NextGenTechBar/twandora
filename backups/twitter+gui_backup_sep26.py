#Titter + gui
from Tkinter import *
from time import sleep

import os
import tweepy
import requests
import json
from pydora import player
#test import line
from pandora import clientbuilder
import sys
import termios
import getpass
import subprocess


#Global Variable keys (I got these from the twitter app page)
#need to change them for other twitter accounts
consumer_key = "3gI3AIYm8OkxfkU9Er81DZ4Kd"
consumer_secret = "drCThGHlqjHfF3QcFiEWB1LjvsglEiHoiKQ5OeB1UiYCx7PyMl"
access_token = "2462366071-WHcsSVijoOa9tHWokK8ZNd1zQRJSseJPojGQGut"
access_token_secret = "gtbePKnCgIl6UpkrUGLks3o77WYgKoWeRnVKXOLIg2kQ4"






def main():
    def search(tweet):
        print ("running")
        client = get_client()
        #self.stations = self.client.get_station_list()
        print("Connected")

        search = (client.search(tweet,include_genre_stations=True))
        #print (self.search.artists[0].artist)
        print ("About to return station")
        #return (self.search.artists[0].artist)

        #return search
        artists_score = 0
        songs_score = 0
        genre_score = 0

        print(search)

        if (len(search.artists) != 0):
            artists_score = search.artists[0].score
            artists_token = search.artists[0].token
            artists_name = search.artists[0].artist
            print(artists_name)
                    
        if (len(search.songs) != 0):

            songs_score = search.songs[0].score
            songs_token = search.songs[0].token
            songs_name = search.songs[0].song_name
            print(songs_name)

        if (len(search.genre_stations) != 0):
     
            genre_score = search.genre_stations[0].score
            genre_token = search.genre_stations[0].token
            genre_name = search.genre_stations[0].station_name
            print(genre_name)

        print("Done sorting")

        if (artists_score > 80):
            print("Returning artist: ", artists_name)
            return artists_name
        elif(genre_score > 80):
            print("Returning genre: ", genre_name)
            return genre_name
        elif(songs_score > 80):
            print("Retruning song: ", songs_name)
            return songs_name

        else:
            print("Error: no station matches your request")
            return ("error")


    def get_client():
        cfg_file = os.environ.get("PYDORA_CFG", "")
        builder = clientbuilder.PydoraConfigFileBuilder(cfg_file)
        if builder.file_exists:
            return builder.build()

        builder = clientbuilder.PianobarConfigFileBuilder()
        if builder.file_exists:
            return builder.build()

        if not client:
            Screen.print_error("No valid config found")
            sys.exit(1)


    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    #GUI Stuff
    root = Tk()
    S = Scrollbar(root)
    var = StringVar()
    var.set('Scanning for tweets')
    L = Label(root, anchor=NW,justify=LEFT, textvariable = var, height=20, width=50, relief=RIDGE, fg="red", font=("Helvetica", 16), )
    L.pack()
    S.pack(side=RIGHT, fill=Y)
    root.update_idletasks()


    
    #work on this
    def update_gui(station):
        var.set(station)
        root.update_idletasks()

    #finish save_stuff first
    def tweet_sort():
        pass


    def save_stuff(name, time, body, station):
        #We want to keep name, timestamp, tweet, and the returned station in a file

        string = ('\nname: ' + name + '\ntime: ' + time + '\ntweet: ' + body + 'station: ' + station)

        f = open('SAVE_FILE', 'a')
        f.write('\n' + string)


        '''
        f = open('SAVE_FILE', 'r+')
        f.append(lst)
        json.dump(lst, f)
        '''




    
    #Acual main file. This is what runs when you execute the file
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print 'Error! Failed to get request token.'

    request_token = auth.request_token


    class StdOutListener(tweepy.StreamListener):
        def on_data(self,data):
            tweet = json.loads(data)

            
            
            #print (tweet)
            #this has a lot of valuable information
            
            temp = tweet['text'] #prints out contents of tweet
            lst = temp.split('#')  #gets rid of #hemmingson
            print lst
            body = lst[0]
            print body
            
            #gets the user that sent the tweet
            user = tweet.get('user')
            name = user['screen_name']
            
            
            #gets the time the tweet was created.
            #Printed in tweet to prevent duplicate tweet errors
            time = tweet['created_at']
            time = time[:-10]
            '''
            #Grabs an image from local device and posts it
            image = os.path.abspath('/home/pi/Desktop/something.png')
            #prints out the screen name
            #api.update_status("@" + name + "\nRetweet Test\n" + time + "/n")
            api.update_with_media(image, status="@" + name + "\nRetweet Test\n" + time + "/n")
            '''

            
            station = search(body)
            print ("Recieved the station")
            print (station)

            save_stuff(name, time, body, station)
                        
            var.set(station)
            root.update_idletasks()
            
        
        def on_error(self, status):
            print (status)



    if __name__ == '__main__':
        l = StdOutListener()
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        print "Scanning for Hemmingson Playlist Requests"
        stream = tweepy.Stream(auth, l)
        stream.filter(track=['ngtb,Ngtb,NGTB,Hemmingson,hemmingson,hemmingson playlist,Hemmingson playlist,Hemmingson Playlist, hemmingsonplaylist,Hemmingsonplaylist,HemmingsonPlaylist'])




main()
