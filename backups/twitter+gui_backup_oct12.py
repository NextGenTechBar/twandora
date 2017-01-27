#Titter + gui
from Tkinter import *
from time import sleep

import os
import tweepy
import requests
import json
from pydora import player
from pandora import clientbuilder
import sys
import termios
import getpass
import subprocess
import time

#import for gui
import Tkinter

#import for processes using rabbitmq
import pika
from multiprocessing import Process, Manager


#Global Variable keys (I got these from the twitter app page)
#need to change them for other twitter accounts
'''
consumer_key = "3gI3AIYm8OkxfkU9Er81DZ4Kd"
consumer_secret = "drCThGHlqjHfF3QcFiEWBEnter Text Here1LjvsglEiHoiKQ5OeB1UiYCx7PyMl"
access_token = "2462366071-WHcsSVijoOa9tHWokK8ZNd1zQRJSseJPojGQGut"
access_token_secret = "gtbePKnCgIl6UpkrUGLks3o77WYgKoWeRnVKXOLIg2kQ4"
'''

consumer_key = "3gI3AIYm8OkxfkU9Er81DZ4Kd"
consumer_secret = "drCThGHlqjHfF3QcFiEWB1LjvsglEiHoiKQ5OeB1UiYCx7PyMl"
access_token = "2462366071-WHcsSVijoOa9tHWokK8ZNd1zQRJSseJPojGQGut"
access_token_secret = "gtbePKnCgIl6UpkrUGLks3o77WYgKoWeRnVKXOLIg2kQ4"


class simpleapp_tk(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self, textvariable=self.entryVariable)
        self.entry.grid(column=0, row=0, sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter Text Here")

        button = Tkinter.Button(self, text=u"Click here",
                                command=self.OnButtonClick)
        button.grid(column=1, row=0)

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.labelVariable,
                              anchor="nw", fg="white", bg="#335",
                              width=100, height=25,
                              justify='right',
                              cursor='gumby', font=("Times",20))
        label.grid(column=0, row=1, columnspan=2, sticky='EW')
        self.labelVariable.set(u"Hello")


        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)



    def OnButtonClick(self):
        i = 0
        lst = []
        string = ''
        
        station_list = open('/home/pi/Desktop/pydora-test/DICT_SAVE', 'r')
        for station in station_list:
            lst.append(station)
            string = string + station
        i = 0
        #print (string)
        self.labelVariable.set(string)
        '''
        for i in range (len(lst)):
            print (lst[i])
            self.labelVariable.set(lst[i])
         '''   

        '''
        self.labelVariable.set(self.entryVariable.get()+"You clicked the button!")
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        '''
    def OnPressEnter(self, event):
        self.labelVariable.set(self.entryVariable.get()+"You pressed enter")
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)




def twitter():
    def search(tweet):
        print ("running")
        client = get_client()
        print("Connected")

        search = (client.search(tweet,include_genre_stations=True))
        print ("About to sort stations")
        artists_score = 0
        songs_score = 0
        genre_score = 0

        print(search)

        if (len(search.artists) != 0):
            artists_score = search.artists[0].score
            artists_token = search.artists[0].token
            artists_name = search.artists[0].artist
            print("did artist search "+artists_name)
        print("#1")      
        if (len(search.songs) != 0):

            songs_score = search.songs[0].score
            songs_token = search.songs[0].token
            songs_name = search.songs[0].song_name
            print("did song search " +songs_name)
        print("#2")
        if (len(search.genre_stations) != 0):
     
            genre_score = search.genre_stations[0].score
            genre_token = search.genre_stations[0].token
            genre_name = search.genre_stations[0].station_name
            print("did genre search "+genre_name)
        print ("#3")
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


    def save_stuff(name, time, body, station):
        #We want to keep name, timestamp, tweet, and the returned station in a file

        
        string = ('\nname: ' + name + '\ntime: ' + time + '\ntweet: ' + body + 'station: ' + station)

        f = open('/home/pi/Desktop/pydora-test/SAVE_FILE', 'a')
        f.write('\n' + string)

        s = open('/home/pi/Desktop/pydora-test/STATION_SAVE', 'a')
        s.write(station + '\n')
        
        

   
    #Acual main file. This is what runs when you execute the file
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

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
            if station != ('error'):
                save_stuff(name, time, body, station)
        
        def on_error(self, status):
            print (status)
    
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    print "Scanning for Hemmingson Playlist Requests"
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['hemmingson'])
    while(stream.running):
        #time.sleep(0)
        pass



def gui():
    app = simpleapp_tk(None)
    app.title('Test Stuff')
    app.mainloop()



def sort():
    SAVE_BUFFER = {}
    
    def dict_to_string(dictionary):
        total_string = ''
        for key in dictionary:
            string = key + "  - - - - - - - - - - - - - - - - - - - - -"
            string = string[:30]
            count = str(dictionary[key])
            total_string = total_string + string + count + '\n'
        return total_string
    
    def __init__():
        if len(SAVE_BUFFER) == 0:
            station_list = open('/home/pi/Desktop/pydora-test/STATION_SAVE', 'r')
            for station in station_list:
                #print (station)
                temp = station[:len(station)-1]
                if temp != '':
                    if temp in SAVE_BUFFER.keys():
                        SAVE_BUFFER[temp] = SAVE_BUFFER[temp] + 1
                    else:
                        SAVE_BUFFER[temp] = 1
    while True:
        __init__()
        dictionary = open('/home/pi/Desktop/pydora-test/DICT_SAVE', 'w')
        string = dict_to_string(SAVE_BUFFER)
        #print (string)
        dictionary.write(string)
        time.sleep(2)
    
    '''
    while (True):
        station_list = open('STATION_SAVE', 'r')
        for station in station_list:
            print station

        time.sleep(20)
    '''      

def twitter_process():
    twitter()



if (__name__ == "__main__"):
    p = Process(target=twitter_process, args=())
    q = Process(target=gui, args=())
    r = Process(target=sort, args=())

    p.start()
    q.start()
    r.start()

    p.join()
    q.join()
    r.join()






    

